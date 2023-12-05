import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class MediumApiClient:
    API_URL = "https://api.medium.com/v1"
    USER_ENDPOINT = "/me"
    PUBLICATIONS_ENDPOINT = "/publications"
    USERS_ENDPOINT = "/users"
    POSTS_ENDPOINT = "/posts"
    GRAPHQL_ENDPOINT = "https://medium.com/_/graphql"

    def __init__(
        self,
        api_token,
        use_graph_ql=False,
        graphql_entities=["posts", "publications"],
        search_limit=10,
    ):
        self.use_graph_ql = use_graph_ql
        if use_graph_ql:
            self.search_limit = search_limit
            self.graphql_entities = graphql_entities
            self.API_URL = self.GRAPHQL_ENDPOINT
            self.headers = {
                "graphql-operation": "SearchQuery",
                "Content-Type": "application/json",
            }
        else:
            self.headers = {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
            }

    def is_graph_ql_used(self):
        return self.use_graph_ql

    def get(self, url, params={}):
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def post(self, params={}):
        response = requests.post(self.API_URL, headers=self.headers, json=params)

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def get_user(self):
        url = f"{self.API_URL}{self.USER_ENDPOINT}"
        return self.get(url)

    def get_user_publications(self, user_id):
        url = (
            f"{self.API_URL}{self.USERS_ENDPOINT}/{user_id}{self.PUBLICATIONS_ENDPOINT}"
        )
        return self.get(url)

    def get_graphql_results(self, query):
        ql_query = """
        query SearchQuery($query: String!, $pagingOptions: SearchPagingOptions!, $searchInCollection: Boolean!, $collectionDomainOrSlug: String!, $withUsers: Boolean!, $withTags: Boolean!, $withPosts: Boolean!, $withCollections: Boolean!, $withLists: Boolean!, $peopleSearchOptions: SearchOptions, $postsSearchOptions: SearchOptions, $tagsSearchOptions: SearchOptions, $publicationsSearchOptions: SearchOptions, $listsSearchOptions: SearchOptions) {
          search(query: $query) @skip(if: $searchInCollection) {
            __typename
            ...Search_search
          }
          searchInCollection(query: $query, domainOrSlug: $collectionDomainOrSlug) @include(if: $searchInCollection) {
            __typename
            ...Search_search
          }
        }

        fragment Search_search on Search {
          people(pagingOptions: $pagingOptions, algoliaOptions: $peopleSearchOptions) @include(if: $withUsers) {
            ... on SearchPeople {
              pagingInfo {
                next {
                  limit
                  page
                  __typename
                }
                __typename
              }
              ...SearchPeople_people
              __typename
            }
            __typename
          }
          tags(pagingOptions: $pagingOptions, algoliaOptions: $tagsSearchOptions) @include(if: $withTags) {
            ... on SearchTag {
              pagingInfo {
                next {
                  limit
                  page
                  __typename
                }
                __typename
              }
              ...SearchTags_tags
              __typename
            }
            __typename
          }
          posts(pagingOptions: $pagingOptions, algoliaOptions: $postsSearchOptions) @include(if: $withPosts) {
            ... on SearchPost {
              pagingInfo {
                next {
                  limit
                  page
                  __typename
                }
                __typename
              }
              ...SearchPosts_posts
              __typename
            }
            __typename
          }
          collections(
            pagingOptions: $pagingOptions
            algoliaOptions: $publicationsSearchOptions
          ) @include(if: $withCollections) {
            ... on SearchCollection {
              pagingInfo {
                next {
                  limit
                  page
                  __typename
                }
                __typename
              }
              ...SearchCollections_collections
              __typename
            }
            __typename
          }
          catalogs(pagingOptions: $pagingOptions, algoliaOptions: $listsSearchOptions) @include(if: $withLists) {
            ... on SearchCatalog {
              pagingInfo {
                next {
                  limit
                  page
                  __typename
                }
                __typename
              }
              ...SearchLists_catalogs
              __typename
            }
            __typename
          }
          __typename
        }

        fragment SearchPeople_people on SearchPeople {
          items {
            __typename
            ... on User {
              algoliaObjectId
              __typename
              id
            }
            ...UserFollowInline_user
          }
          queryId
          __typename
        }

        fragment UserFollowInline_user on User {
          id
          name
          bio
          mediumMemberAt
          ...UserAvatar_user
          ...UserFollowButton_user
          ...userUrl_user
          ...useIsVerifiedBookAuthor_user
          __typename
        }

        fragment UserAvatar_user on User {
          __typename
          id
          imageId
          mediumMemberAt
          membership {
            tier
            __typename
            id
          }
          name
          username
          ...userUrl_user
        }

        fragment userUrl_user on User {
          __typename
          id
          customDomainState {
            live {
              domain
              __typename
            }
            __typename
          }
          hasSubdomain
          username
        }

        fragment UserFollowButton_user on User {
          ...UserFollowButtonSignedIn_user
          ...UserFollowButtonSignedOut_user
          __typename
          id
        }

        fragment UserFollowButtonSignedIn_user on User {
          id
          name
          __typename
        }

        fragment UserFollowButtonSignedOut_user on User {
          id
          ...SusiClickable_user
          __typename
        }

        fragment SusiClickable_user on User {
          ...SusiContainer_user
          __typename
          id
        }

        fragment SusiContainer_user on User {
          ...SignInOptions_user
          ...SignUpOptions_user
          __typename
          id
        }

        fragment SignInOptions_user on User {
          id
          name
          __typename
        }

        fragment SignUpOptions_user on User {
          id
          name
          __typename
        }

        fragment useIsVerifiedBookAuthor_user on User {
          verifications {
            isBookAuthor
            __typename
          }
          __typename
          id
        }

        fragment SearchTags_tags on SearchTag {
          items {
            id
            algoliaObjectId
            ...TopicPill_tag
            __typename
          }
          queryId
          __typename
        }

        fragment TopicPill_tag on Tag {
          __typename
          id
          displayTitle
          normalizedTagSlug
        }

        fragment SearchPosts_posts on SearchPost {
          items {
            id
            algoliaObjectId
            ...PostPreview_post
            __typename
          }
          queryId
          __typename
        }

        fragment PostPreview_post on Post {
          id
          creator {
            ...PostPreview_user
            __typename
            id
          }
          collection {
            ...CardByline_collection
            ...ExpandablePostByline_collection
            __typename
            id
          }
          ...InteractivePostBody_postPreview
          firstPublishedAt
          isLocked
          isSeries
          latestPublishedAt
          inResponseToCatalogResult {
            __typename
          }
          pinnedAt
          pinnedByCreatorAt
          previewImage {
            id
            focusPercentX
            focusPercentY
            __typename
          }
          readingTime
          sequence {
            slug
            __typename
          }
          title
          uniqueSlug
          ...CardByline_post
          ...PostFooterActionsBar_post
          ...InResponseToEntityPreview_post
          ...PostScrollTracker_post
          ...HighDensityPreview_post
          __typename
        }

        fragment PostPreview_user on User {
          __typename
          name
          username
          ...CardByline_user
          ...ExpandablePostByline_user
          id
        }

        fragment CardByline_user on User {
          __typename
          id
          name
          username
          mediumMemberAt
          socialStats {
            followerCount
            __typename
          }
          ...useIsVerifiedBookAuthor_user
          ...userUrl_user
          ...UserMentionTooltip_user
        }

        fragment UserMentionTooltip_user on User {
          id
          name
          username
          bio
          imageId
          mediumMemberAt
          membership {
            tier
            __typename
            id
          }
          ...UserAvatar_user
          ...UserFollowButton_user
          ...useIsVerifiedBookAuthor_user
          __typename
        }

        fragment ExpandablePostByline_user on User {
          __typename
          id
          name
          imageId
          ...userUrl_user
          ...useIsVerifiedBookAuthor_user
        }

        fragment CardByline_collection on Collection {
          name
          ...collectionUrl_collection
          __typename
          id
        }

        fragment collectionUrl_collection on Collection {
          id
          domain
          slug
          __typename
        }

        fragment ExpandablePostByline_collection on Collection {
          __typename
          id
          name
          domain
          slug
        }

        fragment InteractivePostBody_postPreview on Post {
          extendedPreviewContent(
            truncationConfig: {previewParagraphsWordCountThreshold: 400, minimumWordLengthForTruncation: 150, truncateAtEndOfSentence: true, showFullImageCaptions: true, shortformPreviewParagraphsWordCountThreshold: 30, shortformMinimumWordLengthForTruncation: 30}
          ) {
            bodyModel {
              ...PostBody_bodyModel
              __typename
            }
            isFullContent
            __typename
          }
          __typename
          id
        }

        fragment PostBody_bodyModel on RichText {
          sections {
            name
            startIndex
            textLayout
            imageLayout
            backgroundImage {
              id
              originalHeight
              originalWidth
              __typename
            }
            videoLayout
            backgroundVideo {
              videoId
              originalHeight
              originalWidth
              previewImageId
              __typename
            }
            __typename
          }
          paragraphs {
            id
            ...PostBodySection_paragraph
            __typename
          }
          ...normalizedBodyModel_richText
          __typename
        }

        fragment PostBodySection_paragraph on Paragraph {
          name
          ...PostBodyParagraph_paragraph
          __typename
          id
        }

        fragment PostBodyParagraph_paragraph on Paragraph {
          name
          type
          ...ImageParagraph_paragraph
          ...TextParagraph_paragraph
          ...IframeParagraph_paragraph
          ...MixtapeParagraph_paragraph
          ...CodeBlockParagraph_paragraph
          __typename
          id
        }

        fragment ImageParagraph_paragraph on Paragraph {
          href
          layout
          metadata {
            id
            originalHeight
            originalWidth
            focusPercentX
            focusPercentY
            alt
            __typename
          }
          ...Markups_paragraph
          ...ParagraphRefsMapContext_paragraph
          ...PostAnnotationsMarker_paragraph
          __typename
          id
        }

        fragment Markups_paragraph on Paragraph {
          name
          text
          hasDropCap
          dropCapImage {
            ...MarkupNode_data_dropCapImage
            __typename
            id
          }
          markups {
            ...Markups_markup
            __typename
          }
          __typename
          id
        }

        fragment MarkupNode_data_dropCapImage on ImageMetadata {
          ...DropCap_image
          __typename
          id
        }

        fragment DropCap_image on ImageMetadata {
          id
          originalHeight
          originalWidth
          __typename
        }

        fragment Markups_markup on Markup {
          type
          start
          end
          href
          anchorType
          userId
          linkMetadata {
            httpStatus
            __typename
          }
          __typename
        }

        fragment ParagraphRefsMapContext_paragraph on Paragraph {
          id
          name
          text
          __typename
        }

        fragment PostAnnotationsMarker_paragraph on Paragraph {
          ...PostViewNoteCard_paragraph
          __typename
          id
        }

        fragment PostViewNoteCard_paragraph on Paragraph {
          name
          __typename
          id
        }

        fragment TextParagraph_paragraph on Paragraph {
          type
          hasDropCap
          codeBlockMetadata {
            mode
            lang
            __typename
          }
          ...Markups_paragraph
          ...ParagraphRefsMapContext_paragraph
          __typename
          id
        }

        fragment IframeParagraph_paragraph on Paragraph {
          type
          iframe {
            mediaResource {
              id
              iframeSrc
              iframeHeight
              iframeWidth
              title
              __typename
            }
            __typename
          }
          layout
          ...Markups_paragraph
          __typename
          id
        }

        fragment MixtapeParagraph_paragraph on Paragraph {
          type
          mixtapeMetadata {
            href
            mediaResource {
              mediumCatalog {
                id
                __typename
              }
              __typename
            }
            __typename
          }
          ...GenericMixtapeParagraph_paragraph
          __typename
          id
        }

        fragment GenericMixtapeParagraph_paragraph on Paragraph {
          text
          mixtapeMetadata {
            href
            thumbnailImageId
            __typename
          }
          markups {
            start
            end
            type
            href
            __typename
          }
          __typename
          id
        }

        fragment CodeBlockParagraph_paragraph on Paragraph {
          codeBlockMetadata {
            lang
            mode
            __typename
          }
          __typename
          id
        }

        fragment normalizedBodyModel_richText on RichText {
          paragraphs {
            ...normalizedBodyModel_richText_paragraphs
            __typename
          }
          sections {
            startIndex
            ...getSectionEndIndex_section
            __typename
          }
          ...getParagraphStyles_richText
          ...getParagraphSpaces_richText
          __typename
        }

        fragment normalizedBodyModel_richText_paragraphs on Paragraph {
          markups {
            ...normalizedBodyModel_richText_paragraphs_markups
            __typename
          }
          codeBlockMetadata {
            lang
            mode
            __typename
          }
          ...getParagraphHighlights_paragraph
          ...getParagraphPrivateNotes_paragraph
          __typename
          id
        }

        fragment normalizedBodyModel_richText_paragraphs_markups on Markup {
          type
          __typename
        }

        fragment getParagraphHighlights_paragraph on Paragraph {
          name
          __typename
          id
        }

        fragment getParagraphPrivateNotes_paragraph on Paragraph {
          name
          __typename
          id
        }

        fragment getSectionEndIndex_section on Section {
          startIndex
          __typename
        }

        fragment getParagraphStyles_richText on RichText {
          paragraphs {
            text
            type
            __typename
          }
          sections {
            ...getSectionEndIndex_section
            __typename
          }
          __typename
        }

        fragment getParagraphSpaces_richText on RichText {
          paragraphs {
            layout
            metadata {
              originalHeight
              originalWidth
              id
              __typename
            }
            type
            ...paragraphExtendsImageGrid_paragraph
            __typename
          }
          ...getSeriesParagraphTopSpacings_richText
          ...getPostParagraphTopSpacings_richText
          __typename
        }

        fragment paragraphExtendsImageGrid_paragraph on Paragraph {
          layout
          type
          __typename
          id
        }

        fragment getSeriesParagraphTopSpacings_richText on RichText {
          paragraphs {
            id
            __typename
          }
          sections {
            ...getSectionEndIndex_section
            __typename
          }
          __typename
        }

        fragment getPostParagraphTopSpacings_richText on RichText {
          paragraphs {
            type
            layout
            text
            codeBlockMetadata {
              lang
              mode
              __typename
            }
            __typename
          }
          sections {
            ...getSectionEndIndex_section
            __typename
          }
          __typename
        }

        fragment CardByline_post on Post {
          ...DraftStatus_post
          ...Star_post
          ...shouldShowPublishedInStatus_post
          __typename
          id
        }

        fragment DraftStatus_post on Post {
          id
          pendingCollection {
            id
            creator {
              id
              __typename
            }
            ...BoldCollectionName_collection
            __typename
          }
          statusForCollection
          creator {
            id
            __typename
          }
          isPublished
          __typename
        }

        fragment BoldCollectionName_collection on Collection {
          id
          name
          __typename
        }

        fragment Star_post on Post {
          id
          creator {
            id
            __typename
          }
          __typename
        }

        fragment shouldShowPublishedInStatus_post on Post {
          statusForCollection
          isPublished
          __typename
          id
        }

        fragment PostFooterActionsBar_post on Post {
          id
          visibility
          allowResponses
          postResponses {
            count
            __typename
          }
          isLimitedState
          creator {
            id
            __typename
          }
          collection {
            id
            __typename
          }
          ...MultiVote_post
          ...PostSharePopover_post
          ...OverflowMenuButtonWithNegativeSignal_post
          ...PostPageBookmarkButton_post
          __typename
        }

        fragment MultiVote_post on Post {
          id
          creator {
            id
            ...SusiClickable_user
            __typename
          }
          isPublished
          ...SusiClickable_post
          collection {
            id
            slug
            __typename
          }
          isLimitedState
          ...MultiVoteCount_post
          __typename
        }

        fragment SusiClickable_post on Post {
          id
          mediumUrl
          ...SusiContainer_post
          __typename
        }

        fragment SusiContainer_post on Post {
          id
          __typename
        }

        fragment MultiVoteCount_post on Post {
          id
          __typename
        }

        fragment PostSharePopover_post on Post {
          id
          mediumUrl
          title
          isPublished
          isLocked
          ...usePostUrl_post
          ...FriendLink_post
          __typename
        }

        fragment usePostUrl_post on Post {
          id
          creator {
            ...userUrl_user
            __typename
            id
          }
          collection {
            id
            domain
            slug
            __typename
          }
          isSeries
          mediumUrl
          sequence {
            slug
            __typename
          }
          uniqueSlug
          __typename
        }

        fragment FriendLink_post on Post {
          id
          ...SusiClickable_post
          ...useCopyFriendLink_post
          __typename
        }

        fragment useCopyFriendLink_post on Post {
          ...usePostUrl_post
          __typename
          id
        }

        fragment OverflowMenuButtonWithNegativeSignal_post on Post {
          id
          visibility
          ...OverflowMenuWithNegativeSignal_post
          __typename
        }

        fragment OverflowMenuWithNegativeSignal_post on Post {
          id
          creator {
            id
            __typename
          }
          collection {
            id
            __typename
          }
          ...OverflowMenuItemUndoClaps_post
          ...AddToCatalogBase_post
          __typename
        }

        fragment OverflowMenuItemUndoClaps_post on Post {
          id
          clapCount
          ...ClapMutation_post
          __typename
        }

        fragment ClapMutation_post on Post {
          __typename
          id
          clapCount
          ...MultiVoteCount_post
        }

        fragment AddToCatalogBase_post on Post {
          id
          isPublished
          __typename
        }

        fragment PostPageBookmarkButton_post on Post {
          ...AddToCatalogBookmarkButton_post
          __typename
          id
        }

        fragment AddToCatalogBookmarkButton_post on Post {
          ...AddToCatalogBase_post
          __typename
          id
        }

        fragment InResponseToEntityPreview_post on Post {
          id
          inResponseToEntityType
          __typename
        }

        fragment PostScrollTracker_post on Post {
          id
          collection {
            id
            __typename
          }
          sequence {
            sequenceId
            __typename
          }
          __typename
        }

        fragment HighDensityPreview_post on Post {
          id
          title
          previewImage {
            id
            focusPercentX
            focusPercentY
            __typename
          }
          extendedPreviewContent(
            truncationConfig: {previewParagraphsWordCountThreshold: 400, minimumWordLengthForTruncation: 150, truncateAtEndOfSentence: true, showFullImageCaptions: true, shortformPreviewParagraphsWordCountThreshold: 30, shortformMinimumWordLengthForTruncation: 30}
          ) {
            subtitle
            __typename
          }
          ...HighDensityFooter_post
          __typename
        }

        fragment HighDensityFooter_post on Post {
          id
          readingTime
          tags {
            ...TopicPill_tag
            __typename
          }
          ...BookmarkButton_post
          ...ExpandablePostCardOverflowButton_post
          ...OverflowMenuButtonWithNegativeSignal_post
          __typename
        }

        fragment BookmarkButton_post on Post {
          visibility
          ...SusiClickable_post
          ...AddToCatalogBookmarkButton_post
          __typename
          id
        }

        fragment ExpandablePostCardOverflowButton_post on Post {
          creator {
            id
            __typename
          }
          ...ExpandablePostCardReaderButton_post
          __typename
          id
        }

        fragment ExpandablePostCardReaderButton_post on Post {
          id
          collection {
            id
            __typename
          }
          creator {
            id
            __typename
          }
          clapCount
          ...ClapMutation_post
          __typename
        }

        fragment SearchCollections_collections on SearchCollection {
          items {
            id
            algoliaObjectId
            ...CollectionFollowInline_collection
            __typename
          }
          queryId
          __typename
        }

        fragment CollectionFollowInline_collection on Collection {
          id
          name
          domain
          shortDescription
          slug
          ...CollectionAvatar_collection
          ...CollectionFollowButton_collection
          __typename
        }

        fragment CollectionAvatar_collection on Collection {
          name
          avatar {
            id
            __typename
          }
          ...collectionUrl_collection
          __typename
          id
        }

        fragment CollectionFollowButton_collection on Collection {
          __typename
          id
          name
          slug
          ...collectionUrl_collection
          ...SusiClickable_collection
        }

        fragment SusiClickable_collection on Collection {
          ...SusiContainer_collection
          __typename
          id
        }

        fragment SusiContainer_collection on Collection {
          name
          ...SignInOptions_collection
          ...SignUpOptions_collection
          __typename
          id
        }

        fragment SignInOptions_collection on Collection {
          id
          name
          __typename
        }

        fragment SignUpOptions_collection on Collection {
          id
          name
          __typename
        }

        fragment SearchLists_catalogs on SearchCatalog {
          items {
            id
            algoliaObjectId
            ...CatalogsListItem_catalog
            __typename
          }
          queryId
          __typename
        }

        fragment CatalogsListItem_catalog on Catalog {
          id
          name
          predefined
          visibility
          creator {
            imageId
            name
            ...userUrl_user
            ...useIsVerifiedBookAuthor_user
            __typename
            id
          }
          ...getCatalogSlugId_Catalog
          ...formatItemsCount_catalog
          ...CatalogsListItemCovers_catalog
          ...CatalogContentMenu_catalog
          ...SaveCatalogButton_catalog
          __typename
        }

        fragment getCatalogSlugId_Catalog on Catalog {
          id
          name
          __typename
        }

        fragment formatItemsCount_catalog on Catalog {
          postItemsCount
          __typename
          id
        }

        fragment CatalogsListItemCovers_catalog on Catalog {
          listItemsConnection: itemsConnection(pagingOptions: {limit: 10}) {
            items {
              catalogItemId
              ...PreviewCatalogCovers_catalogItemV2
              __typename
            }
            __typename
          }
          __typename
          id
        }

        fragment PreviewCatalogCovers_catalogItemV2 on CatalogItemV2 {
          catalogItemId
          entity {
            __typename
            ... on Post {
              visibility
              previewImage {
                id
                alt
                __typename
              }
              __typename
              id
            }
          }
          __typename
        }

        fragment CatalogContentMenu_catalog on Catalog {
          creator {
            ...userUrl_user
            __typename
            id
          }
          ...CatalogContentNonCreatorMenu_catalog
          ...CatalogContentCreatorMenu_catalog
          __typename
          id
        }

        fragment CatalogContentNonCreatorMenu_catalog on Catalog {
          id
          viewerEdge {
            clapCount
            __typename
            id
          }
          ...catalogUrl_catalog
          __typename
        }

        fragment catalogUrl_catalog on Catalog {
          id
          predefined
          ...getCatalogSlugId_Catalog
          creator {
            ...userUrl_user
            __typename
            id
          }
          __typename
        }

        fragment CatalogContentCreatorMenu_catalog on Catalog {
          id
          visibility
          name
          description
          type
          postItemsCount
          predefined
          disallowResponses
          creator {
            ...userUrl_user
            __typename
            id
          }
          ...UpdateCatalogDialog_catalog
          ...catalogUrl_catalog
          __typename
        }

        fragment UpdateCatalogDialog_catalog on Catalog {
          id
          name
          description
          visibility
          type
          __typename
        }

        fragment SaveCatalogButton_catalog on Catalog {
          id
          creator {
            id
            username
            __typename
          }
          viewerEdge {
            id
            isFollowing
            __typename
          }
          ...getCatalogSlugId_Catalog
          __typename
        }
        """
        variables = {
            "query": query,
            "pagingOptions": {"limit": self.search_limit, "page": 0},
            "withUsers": "users" in self.graphql_entities,
            "withTags": "tags" in self.graphql_entities,
            "withPosts": "posts" in self.graphql_entities,
            "withCollections": "publications" in self.graphql_entities,
            "withLists": "lists" in self.graphql_entities,
            "peopleSearchOptions": {
                "filters": "highQualityUser:true OR writtenByHighQulityUser:true",
                "numericFilters": "peopleType!=2",
                "clickAnalytics": True,
                "analyticsTags": ["web-main-content"],
            },
            "postsSearchOptions": {
                "filters": "writtenByHighQualityUser:true",
                "clickAnalytics": True,
                "analyticsTags": ["web-main-content"],
            },
            "publicationsSearchOptions": {
                "clickAnalytics": True,
                "analyticsTags": ["web-main-content"],
            },
            "tagsSearchOptions": {
                "numericFilters": "postCount>=1",
                "clickAnalytics": True,
                "analyticsTags": ["web-main-content"],
            },
            "listsSearchOptions": {
                "clickAnalytics": True,
                "analyticsTags": ["web-main-content"],
            },
            "searchInCollection": False,
            "collectionDomainOrSlug": "medium.com",
        }
        return self.post(
            {"query": ql_query, "variables": variables, "operationName": "SearchQuery"}
        )


def get_client() -> MediumApiClient:
    global client
    assert (api_token := app.config.get("API_TOKEN")), "MEDIUM_API_TOKEN must be set"

    search_api = app.config.get("SEARCH_API_TYPE", "graphql")
    searchable_entities = app.config.get("GRAPHQL_ENTITIES", ["posts", "publications"])
    search_limit = app.config.get("SEARCH_LIMIT", 10)
    use_graph_ql = search_api == "graphql"

    if not client:
        client = MediumApiClient(
            api_token, use_graph_ql, searchable_entities, search_limit
        )

    return client
