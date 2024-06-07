import oracledb
from flask import current_app as app
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from . import UpstreamProviderError

nltk.download('stopwords')
nltk.download('punkt')

porter = PorterStemmer()
stop_words = set(stopwords.words('english'))

client = None

class ADBSClient:
    def __init__(
        self,
        user,
        password,
        dsn,
        fts_columns,
        table_name,
        auto_index_fts_columns,
        connection_type,
        wallet_dir, 
        wallet_password,
    ):
        try:
            if (connection_type == 'mTLS'):
                self.connection = oracledb.connect(
                                            user=user, 
                                            password=password,
                                            dsn=dsn,
                                            wallet_location=wallet_dir,
                                            wallet_password=wallet_password
                                )
            else:
                #for only TLS
                self.connection = oracledb.connect(
                                            user=user,
                                            password=password,
                                            dsn=dsn                                                             
                                )
        except: 
            raise UpstreamProviderError("Error connecting to Oracle Database")

        self.user = user
        self.table_name = table_name
        self.fts_columns = fts_columns.split(",")
        self.auto_index_fts_columns = auto_index_fts_columns
        
        #Index the required FTS_Column, Table and Columns must exist.
        if(self.auto_index_fts_columns == "True"):
            self._create_index_configuration()

            for column in fts_columns:
                self._prepare_fts_index(column)
                print('prepared index for column ', column)
    
    def _create_index_configuration(self):
        cursor = self.connection.cursor()

        indexing_properties = f"""
            begin 
                ctx_ddl.create_preference('{self.table_name}_STEM_FUZZY_PREF', 'BASIC_WORDLIST'); 
                ctx_ddl.set_attribute('{self.table_name}_STEM_FUZZY_PREF','FUZZY_MATCH','ENGLISH');
                ctx_ddl.set_attribute('{self.table_name}_STEM_FUZZY_PREF','FUZZY_SCORE','1');
                ctx_ddl.set_attribute('{self.table_name}_STEM_FUZZY_PREF','FUZZY_NUMRESULTS','5000');
                ctx_ddl.set_attribute('{self.table_name}_STEM_FUZZY_PREF','SUBSTRING_INDEX','TRUE');
                ctx_ddl.set_attribute('{self.table_name}_STEM_FUZZY_PREF','STEMMER','ENGLISH');
            end;
        """

        cursor.execute(indexing_properties)

        self.connection.commit()


    def _prepare_fts_index(self, column):
        cursor = self.connection.cursor()

        create_index = f"""
            create index {self.table_name + "_" + column + "_fts_index"} on {self.table_name}({column}) indextype is ctxsys.context parameters ('Wordlist {self.user}.{self.table_name}_STEM_FUZZY_PREF')
        """

        cursor.execute(create_index)

        self.connection.commit()

    
    def get_connection(self):

        return self.connection

    
    def search(self, query):

        query_preprocessed = self._preprocess_query(query)

        sql_query = self.create_sql_query(self.fts_columns, self.table_name)

        cursor = self.connection.cursor()

        response = cursor.execute(sql_query, {'query_value': query_preprocessed})

        columns = [desc[0] for desc in cursor.description]

        results = []
        for row in response.fetchall():
            processed_row = {}
            for idx, value in enumerate(row):
                # Convert fts-column from LOB to string if needed
                if isinstance(value, oracledb.LOB):
                    value = value.read()
                processed_row[columns[idx]] = value
            results.append(processed_row)

        print(results)
        return results

    def create_sql_query(self, fts_columns, table_name):
        
        sql_query = f"""
            SELECT *
            FROM {table_name}
            WHERE """
        
        contains_clauses = ""

        for i,column in enumerate(fts_columns):
            if i == 0:
                contains_clauses = contains_clauses +  f"CONTAINS({column}, :query_value, {i+1}) > 0"
            else:
                contains_clauses = contains_clauses +  f" OR CONTAINS({column}, :query_value, {i+1}) > 0"

        sql_query = sql_query + contains_clauses

        return sql_query

    
    def _preprocess_query(self, query):
        words = word_tokenize(query.lower())

        # Remove stop words and stem words
        filtered_words = [porter.stem(word) for word in words if word not in stop_words]

        # Join the stemmed words back into a sentence
        preprocessed_query = 'or '.join(map(lambda word: f"fuzzy({word}) ", filtered_words))

        return preprocessed_query


def get_client():
    global client
    if not client:
        assert (user := app.config.get("USER")), "USER must be set"
        assert (password := app.config.get("PASSWORD")), "PASSWORD must be set"
        assert (dsn := app.config.get("DSN")), "DSN must be set"
        assert (table_name := app.config.get("TABLE_NAME")), "TABLE_NAME must be set"
        assert (wallet_dir := app.config.get("WALLET_DIR")), "WALLET_DIR must be set (None for TLS)"
        assert (wallet_password := app.config.get("WALLET_PASSWORD")), "WALLET_PASSWORD must be set (None for TLS)"
        assert (fts_columns := app.config.get("FTS_COLUMN_LIST")), "FTS_COLUMNS must be set"
        assert (auto_index_fts_columns := app.config.get("AUTO_INDEX_FTS_COLUMNS")), "AUTO_INDEX_FTS_COLUMNS must be set"
        assert (connection_type := app.config.get("CONNECTION_TYPE")), "CONNECTION_TYPE musst be set, mTLS or TLS"

        client = ADBSClient(
            user,
            password,
            dsn,
            fts_columns,
            table_name,
            auto_index_fts_columns,
            connection_type,
            wallet_dir,
            wallet_password
        )
        
    return client

