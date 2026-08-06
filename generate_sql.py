import json

def main():
    with open('updated_workflow_38.json', 'r', encoding='utf-8') as f:
        json_content = f.read()

    sql = f"""
BEGIN;
UPDATE workflows 
SET workflow_definition = $$ {json_content} $$::json 
WHERE id = 38;

UPDATE workflow_definitions 
SET workflow_json = $$ {json_content} $$::json 
WHERE workflow_id = 38;
COMMIT;
"""
    with open('apply_update.sql', 'w', encoding='utf-8') as f:
        f.write(sql)

if __name__ == "__main__":
    main()
