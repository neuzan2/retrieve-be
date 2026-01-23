erDiagram
    CLIENT ||--o{ PROJECT : "has"
    CLIENT ||--o{ FILE_TRANSFER_LOG : "receives"
    CLIENT ||--o{ GROUP : "owns"

    PROJECT ||--o{ PROJECT_TYPE : "has"
    PROJECT ||--o{ REQUEST : "contains"
    PROJECT ||--o{ VALIDATION_RESULT : "validates"
    PROJECT ||--o{ GROUP : "organizes"
    PROJECT ||--o{ ROSTER : "generates"
    PROJECT ||--o{ FILE_LOAD_SUMMARY : "produces"
    PROJECT ||--|| HEALTH_PLAN_LETTER : "requires"

    MASTER_ADDRESS ||--o{ SITE : "normalizes_to"
    MASTER_ADDRESS ||--o{ ADDRESS_NORMALIZATION_RESULT : "has"

    SITE ||--o{ SITE : "is_master_of"
    SITE ||--o{ REQUEST : "receives"
    SITE ||--o{ VENDOR_SITE : "maps_to"
    SITE ||--o{ SITE_ID_HISTORY : "tracks"
    SITE ||--o{ GROUP : "groups_as"

    MEMBER ||--o{ REQUEST : "requests"
    PROVIDER ||--o{ REQUEST : "services"

    REQUEST ||--o{ DEDUPE_RESULT : "deduplicates"
    REQUEST ||--o{ MATCH_RESULT : "matches"

    GROUP ||--o{ REQUEST : "groups"
    GROUP ||--o{ GROUP_AUDIT : "audits"

    VENDOR ||--o{ VENDOR_SITE : "operates"
    VENDOR ||--o{ MATCH_RESULT : "matched_to"
    VENDOR ||--o{ ROSTER : "receives"
    VENDOR ||--o{ VENDOR_SITE_TABLE_INGESTION : "provides"

    VENDOR_SITE }o--|| SITE : "represents"
    VENDOR_SITE }o--|| VENDOR : "belongs_to"

    ROSTER ||--o{ ROSTER_DISTRIBUTION_LOG : "distributes"

    USER ||--o{ GROUP_AUDIT : "audits"
    USER ||--o{ SITE_ID_HISTORY : "merges"
    USER ||--o{ SYSTEM_AUDIT_LOG : "performs"
    USER ||--o{ HEALTH_PLAN_LETTER : "uploads"

    DEDUPE_RULE ||--o{ DEDUPE_RESULT : "applies"
    MATCH_RULE ||--o{ MATCH_RESULT : "applies"

    CLIENT {
        int client_id PK
        string client_name
        string client_code UK
        string sftp_folder_location
        bool is_active
        datetime created_timestamp
    }

    PROJECT {
        int project_id PK
        int client_id FK
        string project_name
        date project_start_date
        date project_end_date
        date revised_project_end_date
        enum audit_type
        bool duplicate_logic
        bool flr_required
        bool flr_approved
        int program_year
        enum project_status
        bool health_plan_letter_uploaded
        datetime created_timestamp
    }

    PROJECT_TYPE {
        int project_type_id PK
        int project_id FK
        enum project_type
        string hca_contract_number
        datetime created_timestamp
    }

    MASTER_ADDRESS {
        int address_id PK
        string address_line_1
        string address_line_2
        string city
        string state
        string zip5
        string zip4
        string delivery_line_1
        string delivery_line_2
        string normalized_city
        string normalized_state
        string normalized_zip5
        string normalized_zip4
        string canonical_address_hash UK
        decimal normalization_confidence
        string normalization_status
        datetime created_timestamp
    }

    ADDRESS_NORMALIZATION_RESULT {
        int normalization_result_id PK
        int address_id FK
        datetime normalization_timestamp
        string normalization_engine
        bool normalization_passed
        string error_code
        string error_message
        json raw_response
    }

    SITE {
        int site_id PK
        int address_id FK
        int master_site_id FK
        string site_name
        string npi
        string tin
        bool centralized_processing
        datetime created_timestamp
    }

    SITE_ID_HISTORY {
        int history_id PK
        int site_id FK
        int old_site_id
        int new_site_id
        string merge_reason
        int merged_by_user_id FK
        datetime merge_timestamp
    }

    MEMBER {
        int member_id PK
        string member_external_id
        string first_name
        string last_name
        date date_of_birth
        datetime created_timestamp
    }

    PROVIDER {
        int provider_id PK
        string provider_name
        string npi
        string tin
        datetime created_timestamp
    }

    REQUEST {
        int request_id PK
        int project_id FK
        int member_id FK
        int provider_id FK
        int site_id FK
        int group_id FK
        decimal chart_score
        enum request_status
        enum cancellation_code
        datetime cancellation_timestamp
        string original_provider_name
        string original_address_line_1
        string original_phone
        string original_fax
        datetime created_timestamp
    }

    GROUP {
        int group_id PK
        int project_id FK
        int client_id FK
        int group_address_id FK
        bool centralized_processing_flag
        string primary_phone
        string primary_fax
        string source_logic_version
        datetime created_timestamp
    }

    GROUP_AUDIT {
        int audit_id PK
        int group_id FK
        string action
        int changed_by_user_id FK
        datetime change_timestamp
        json change_details
    }

    DEDUPE_RULE {
        int dedupe_rule_id PK
        string rule_name
        string rule_description
        bool is_active
        datetime created_timestamp
    }

    DEDUPE_RESULT {
        int dedupe_result_id PK
        int request_id FK
        int duplicate_of_request_id FK
        bool is_duplicate
        int dedupe_rule_id FK
        string chart_score_comparison
        datetime dedupe_timestamp
    }

    VENDOR {
        int vendor_id PK
        string vendor_name UK
        string vendor_type
        bool is_active
        datetime created_timestamp
    }

    VENDOR_SITE {
        int vendor_site_id PK
        int vendor_id FK
        int site_id FK
        string vendor_site_external_id
        bool processing_site_indicator
        string parent_site_identifier
        json operating_model_attributes
        int ingestion_version
        bool is_active
        datetime created_timestamp
    }

    VENDOR_SITE_TABLE_INGESTION {
        int ingestion_id PK
        int vendor_id FK
        string file_name
        datetime ingestion_timestamp
        int ingestion_version
        int total_rows_processed
        int rows_added
        int rows_edited
        int rows_deleted
        int rows_rejected
        string ingestion_status
        json error_details
    }

    MATCH_RULE {
        int match_rule_id PK
        string rule_name
        string rule_description
        int rule_priority
        bool is_active
        datetime created_timestamp
    }

    MATCH_RESULT {
        int match_result_id PK
        int request_id FK
        int matched_vendor_id FK
        decimal match_confidence_score
        decimal address_match_score
        decimal site_hierarchy_score
        decimal operational_success_score
        int match_rule_id FK
        bool requires_manual_review
        datetime match_timestamp
    }

    FILE_TRANSFER_LOG {
        int transfer_id PK
        int client_id FK
        string file_name
        string source_location
        string destination_bucket
        int file_size_bytes
        string transfer_status
        datetime transfer_timestamp
        string error_message
    }

    VALIDATION_RESULT {
        int validation_id PK
        int project_id FK
        datetime validation_timestamp
        bool validation_passed
        int error_count
        json error_details
    }

    FILE_LOAD_SUMMARY {
        int summary_id PK
        int project_id FK
        string file_name
        int total_records
        int records_loaded
        int records_failed
        int addresses_normalized
        int addresses_failed_normalization
        datetime load_timestamp
        string load_status
    }

    ROSTER {
        int roster_id PK
        int project_id FK
        int vendor_id FK
        string roster_name
        string roster_type
        datetime generation_timestamp
        string distribution_status
        datetime distribution_timestamp
        string file_path
    }

    ROSTER_DISTRIBUTION_LOG {
        int distribution_log_id PK
        int roster_id FK
        string distribution_method
        string distribution_status
        datetime distribution_timestamp
        string error_message
    }

    USER {
        int user_id PK
        string username
        string email UK
        string role
        bool is_active
        datetime created_timestamp
        datetime last_login
    }

    SYSTEM_AUDIT_LOG {
        int log_id PK
        int user_id FK
        string action
        string entity_type
        int entity_id
        datetime action_timestamp
        string ip_address
        json details
    }

    HEALTH_PLAN_LETTER {
        int letter_id PK
        int project_id FK
        string letter_name
        string file_path
        datetime upload_timestamp
        int uploaded_by_user_id FK
    }
