---
title: 一个简单的json解析器
date: 2025-04-19 21:59:37
tags:
	- AI编程
---

--

下面的代码是靠deepseek写的一个简单的json解析器。

可以正常工作。

250行左右。

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

typedef enum {
    JSON_NULL,
    JSON_BOOL,
    JSON_NUMBER,
    JSON_STRING,
    JSON_ARRAY,
    JSON_OBJECT
} json_type;

typedef struct json_value json_value;
typedef struct json_object_entry json_object_entry;

struct json_value {
    json_type type;
    union {
        int boolean;
        double number;
        char *string;
        json_value **elements;  // 指针数组
        json_object_entry *members;
    } data;
    size_t count;
};

struct json_object_entry {
    char *key;
    json_value *value;
};

// 词法分析器部分
typedef enum {
    TOKEN_EOF,
    TOKEN_ERROR,
    TOKEN_LBRACE,
    TOKEN_RBRACE,
    TOKEN_LBRACKET,
    TOKEN_RBRACKET,
    TOKEN_COMMA,
    TOKEN_COLON,
    TOKEN_STRING,
    TOKEN_NUMBER,
    TOKEN_TRUE,
    TOKEN_FALSE,
    TOKEN_NULL
} token_type;

typedef struct {
    token_type type;
    char *start;
    size_t length;
} token;

static const char *json = NULL;
static token current_token;

static void skip_whitespace() {
    while (isspace(*json)) json++;
}

static token get_string_token() {
    const char *start = ++json;
    while (*json != '"') {
        if (*json == '\\') json++;
        if (*json == '\0') return (token){TOKEN_ERROR};
        json++;
    }
    token t = {TOKEN_STRING, (char*)start, (size_t)(json - start)};
    json++;
    return t;
}

static token get_number_token() {
    const char *start = json;
    if (*json == '-') json++;
    while (isdigit(*json)) json++;
    if (*json == '.') json++;
    while (isdigit(*json)) json++;
    if (tolower(*json) == 'e') {
        json++;
        if (*json == '+' || *json == '-') json++;
        while (isdigit(*json)) json++;
    }
    return (token){TOKEN_NUMBER, (char*)start, (size_t)(json - start)};
}

static token next_token() {
    skip_whitespace();
    if (*json == '\0') return (token){TOKEN_EOF};

    switch (*json) {
        case '{': json++; return (token){TOKEN_LBRACE};
        case '}': json++; return (token){TOKEN_RBRACE};
        case '[': json++; return (token){TOKEN_LBRACKET};
        case ']': json++; return (token){TOKEN_RBRACKET};
        case ',': json++; return (token){TOKEN_COMMA};
        case ':': json++; return (token){TOKEN_COLON};
        case '"': return get_string_token();
        case 't': json += 4; return (token){TOKEN_TRUE};
        case 'f': json += 5; return (token){TOKEN_FALSE};
        case 'n': json += 4; return (token){TOKEN_NULL};
        default:
            if (*json == '-' || isdigit(*json)) return get_number_token();
            return (token){TOKEN_ERROR};
    }
}

// 语法分析器部分
static json_value *parse_value();
static json_value *parse_array();
static json_value *parse_object();

static json_value *parse_array() {
    json_value *arr = calloc(1, sizeof(json_value));
    arr->type = JSON_ARRAY;

    current_token = next_token();
    while (current_token.type != TOKEN_RBRACKET) {
        json_value *val = parse_value();
        arr->data.elements = realloc(arr->data.elements, (arr->count + 1) * sizeof(json_value*));
        arr->data.elements[arr->count++] = val;

        current_token = next_token();
        if (current_token.type == TOKEN_COMMA) {
            current_token = next_token();
        }
    }
    return arr;
}

static json_value *parse_object() {
    json_value *obj = calloc(1, sizeof(json_value));
    obj->type = JSON_OBJECT;

    current_token = next_token();
    while (current_token.type != TOKEN_RBRACE) {
        if (current_token.type != TOKEN_STRING) break;
        char *key = strndup(current_token.start, current_token.length);

        current_token = next_token();
        if (current_token.type != TOKEN_COLON) break;

        current_token = next_token();
        json_value *val = parse_value();

        obj->data.members = realloc(obj->data.members, (obj->count + 1) * sizeof(json_object_entry));
        obj->data.members[obj->count].key = key;
        obj->data.members[obj->count].value = val;
        obj->count++;

        current_token = next_token();
        if (current_token.type == TOKEN_COMMA) {
            current_token = next_token();
        }
    }
    return obj;
}

static json_value *parse_value() {
    json_value *val = NULL;
    
    switch (current_token.type) {
        case TOKEN_LBRACE: val = parse_object(); break;
        case TOKEN_LBRACKET: val = parse_array(); break;
        case TOKEN_STRING:
            val = calloc(1, sizeof(json_value));
            val->type = JSON_STRING;
            val->data.string = strndup(current_token.start, current_token.length);
            break;
        case TOKEN_NUMBER:
            val = calloc(1, sizeof(json_value));
            val->type = JSON_NUMBER;
            val->data.number = strtod(current_token.start, NULL);
            break;
        case TOKEN_TRUE:
            val = calloc(1, sizeof(json_value));
            val->type = JSON_BOOL;
            val->data.boolean = 1;
            break;
        case TOKEN_FALSE:
            val = calloc(1, sizeof(json_value));
            val->type = JSON_BOOL;
            val->data.boolean = 0;
            break;
        case TOKEN_NULL:
            val = calloc(1, sizeof(json_value));
            val->type = JSON_NULL;
            break;
        default:
            return NULL;
    }
    return val;
}

json_value *json_parse(const char *input) {
    json = input;
    current_token = next_token();
    return parse_value();
}

// 内存释放
void json_free(json_value *val) {
    if (!val) return;
    
    switch (val->type) {
        case JSON_STRING: free(val->data.string); break;
        case JSON_ARRAY:
            for (size_t i = 0; i < val->count; i++) {
                json_free(val->data.elements[i]);
            }
            free(val->data.elements);
            break;
        case JSON_OBJECT:
            for (size_t i = 0; i < val->count; i++) {
                free(val->data.members[i].key);
                json_free(val->data.members[i].value);
            }
            free(val->data.members);
            break;
        default: break;
    }
    free(val);
}

// 打印函数
void print_json(const json_value *val, int indent) {
    static char spaces[] = "                ";
    if (indent > 15) indent = 15;

    switch (val->type) {
        case JSON_NULL: printf("null"); break;
        case JSON_BOOL: printf(val->data.boolean ? "true" : "false"); break;
        case JSON_NUMBER: printf("%g", val->data.number); break;
        case JSON_STRING: printf("\"%s\"", val->data.string); break;
        case JSON_ARRAY:
            printf("[\n");
            for (size_t i = 0; i < val->count; i++) {
                printf("%.*s", indent+2, spaces);
                print_json(val->data.elements[i], indent+2);
                if (i < val->count-1) printf(",");
                printf("\n");
            }
            printf("%.*s]", indent, spaces);
            break;
        case JSON_OBJECT:
            printf("{\n");
            for (size_t i = 0; i < val->count; i++) {
                printf("%.*s\"%s\": ", indent+2, spaces, val->data.members[i].key);
                print_json(val->data.members[i].value, indent+2);
                if (i < val->count-1) printf(",");
                printf("\n");
            }
            printf("%.*s}", indent, spaces);
            break;
    }
}

int main() {
    const char *complex_json = 
    "{"
    "   \"company\": \"Tech Corp\","
    "   \"founded\": 1999,"
    "   \"active\": true,"
    "   \"departments\": ["
    "       {"
    "           \"name\": \"R&D\","
    "           \"budget\": 5e6,"
    "           \"projects\": [\"AI\", \"Robotics\", null],"
    "           \"remote\": false"
    "       },"
    "       {"
    "           \"name\": \"HR\","
    "           \"employees\": ["
    "               {\"id\": 101, \"name\": \"Alice\"},"
    "               {\"id\": 102, \"name\": \"Bob\", \"extras\": [1,2,3]}"
    "           ]"
    "       }"
    "   ],"
    "   \"locations\": [\"China\", \"USA\", \"Germany\"],"
    "   \"ipo\": null,"
    "   \"stock_data\": {"
    "       \"price\": 234.56,"
    "       \"tickers\": [\"TECH\", \"NYSE:TC\"]"
    "   }"
    "}";

    json_value *root = json_parse(complex_json);
    if (root) {
        printf("=== Parsing Successful ===\n");
        print_json(root, 0);
        printf("\n\n");
        
        // 演示数据访问
        if (root->type == JSON_OBJECT) {
            json_value *stock_data = NULL;
            json_value *departments = NULL;
            
            // 查找嵌套值
            for (size_t i = 0; i < root->count; i++) {
                json_object_entry entry = root->data.members[i];
                if (strcmp(entry.key, "stock_data") == 0) {
                    stock_data = entry.value;
                }
                if (strcmp(entry.key, "departments") == 0) {
                    departments = entry.value;
                }
            }
            
            // 打印特定数据
            if (stock_data && stock_data->type == JSON_OBJECT) {
                printf("Stock Price: ");
                for (size_t i = 0; i < stock_data->count; i++) {
                    if (strcmp(stock_data->data.members[i].key, "price") == 0) {
                        print_json(stock_data->data.members[i].value, 0);
                        printf("\n");
                    }
                }
            }
            
            // 遍历部门信息
            if (departments && departments->type == JSON_ARRAY) {
                printf("\nDepartments:\n");
                for (size_t i = 0; i < departments->count; i++) {
                    json_value *dept = departments->data.elements[i];
                    if (dept->type == JSON_OBJECT) {
                        for (size_t j = 0; j < dept->count; j++) {
                            if (strcmp(dept->data.members[j].key, "name") == 0) {
                                printf(" - ");
                                print_json(dept->data.members[j].value, 0);
                                printf("\n");
                            }
                        }
                    }
                }
            }
        }
        
        json_free(root);
    } else {
        printf("Parse failed\n");
    }
    return 0;
}
```

