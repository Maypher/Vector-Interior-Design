# Database

This is the main postgresql database that holds all data related to the website. It uses the following initialization steps:

1. Creates two users for admin and user backends. Identified respectively by `ADMIN_USERNAME` and `ADMIN_PASSWORD` and `USER_USERNAME` and `USER_PASSWORD`.
2. Manually running `python migrations.py migrate` from within the [cli directory in the admin-backend](/backend/src/admin/cli/) to put everything up to date.

# Tables

**Note**: ids are being skipped since they are present in every table.

```mermaid
---
title: "Vector: Interior Design Database"
---
erDiagram
    admin_user {
        string name
        string email
        string password_hash
    }

    session {
        string session_id
        date expires_at
        int user_id FK
    }

    project {
        string name "The name of the project"
        int area "The area in square meters"
        bool public "Is project to be available in the user frontend?"
        bool main_image "The thumbnail for this project"
        string description_es "The description in Spanish"
        string description_en "The description in English"
        float index "The index to order them in the frontend."
    }

    space {
        string name "The name of the space. Just for organization in the admin panel"
        string description_en "The description in Spanish. Not displayed"
        string description_es "The description in English. Not displayed"
        float index "The index to organize spaces inside a single project"
        int project_id FK "The project this space belongs to"
    }

    image {
        string filename "The filename for this image"
        string alt_text_es "The alt text in Spanish"
        string alt_text_en "The alt text in English"
        string description_es "The description in Spanish"
        string description_en "The description in English"
        string description_font "The font for the description"
        bool main_page "Makes this image appear in the main page"
        bool hide_in_project "Hides this image in the project"
        bool sculpture "Marks this image as an sculpture"
        int phone_config FK "How to display this image in a phone. **Not a foreign key, it's a composite type**"
        int desktop_config FK "How to display this image in desktop. **Not a foreign key, it's a composite type**"
        string bg_color "The hex code of the color used for the background of this image"
        float index "The index to organize images inside a space"
    }

    image_phone_config {
        bit(4) borders "The borders of the image in NSEW order"
        enum alignment "Which way to align the image. One of: LEFT, RIGHT, CENTER, OVERFLOW"
        enum description_position "Where the description is relative to the image. One of: N, S, E, W"
        string description_alignment "The alignment of the description. One of tailwind's text-align values"
    }

    image_desktop_config {
        enum group_alignment "Where to align an image when grouped. One of: TOP, MIDDLE, BOTTOM"
        bool group_end "Forces a group to end. Used for consecutive groups"
        int image_size "The size of the image in percentage of its container"
        bit(4) image_borders "The border of the image in NSEW order"
        enum description_position "The position of the description relative to the image. One of: N, S, E, W"
        string description_alignment "The alignment of the text. One of tailwind's text-align values"
        bit(4) description_borders "The borders of the description in NSEW order"
        enum description_logo_position "The logo of the description position. **Not used**. One of: N, S, E, W"
        enum logo_position "The position of the image logo. **Same as above**"
        bit(4) logo_borders "The borders of the logo. **Same as above**"
    }

    sculpture_data {
        int image_id FK "The image to relate this data to"
        string description_es "The description in Spanish"
        string description_en "The description in English"
        string bg_color "The color of the background in hex format"
        float index "The order of the sculptures in the page"
    }

    main_page_config {
        int image_id FK "The image this config relates to"
        string description_es "The description of this image in Spanish"
        string description_en "The description of this image in English"
        string description_font "The font to use for this description"
        float description_font_size "The size of the description. **Deprecated in favor of markdown**"
        string description_alignment "The alignment of the description. One of tailwind's text-align values"
        int image_size "The size of the image in percentage of the container"
        string bg_color "The color of the background in hex format"
        int phone_config FK "The phone configuration. Not actually a FK but a compose type"
        int desktop_config FK "The desktop configuration. Not actually a FK but a compose type"
    }

    main_page_phone_config {
        bit(4) image_borders "The borders of the image in NSEW order"
        enum description_position "The position relative to the image. One of: N, S, E, W"
        enum logo_position "Position relative to the image. **Same values as above**"
        bit(4) logo_borders "Borders of the logo in NSEW order"
        bool overflow "If the image should overflow to the edges of the screen"
    }

    main_page_desktop_config {
        enum image_position "The position of the image in the screen. One of: LEFT, CENTER, RIGHT"
        enum description_position "The position relative to the image. One of: N, S, E, W"
        bit(4) description_border "The borders in NSEW order"
        enum description_logo_position "The position of the logo relative to the description. **Not used**. One of: N, S, E, W"
        bit(4) description_logo_borders "The borders in NSEW order. **Not used**"
        bool overflow "If the image should overflow to the edge of the screen"
    }

    admin_user }o--|| session : has
    project }o--|| space: contains
    space }o--|| image: contains
    image ||--|| image_phone_config: needs
    image ||--|| image_desktop_config: needs
    image |o--|| sculpture_data: "may be"
    image ||--|| main_page_config: "can be"
    main_page_config ||--||main_page_desktop_config : has
    main_page_config ||--|| main_page_phone_config: has
```

# Indexing

Ordering elements isn't as stray forward as it seems. If it's done in a sequential order the following issue arises:

```
1
2
3
4

1
3
2
4
```

In this case moving position two to the second position means having to update all indexes above it. Meaning it has to update 3, 2, and 4. Worse case scenario this becomes an O(n) operation.

To solve this float indexing is implemented. Where to move an item only that item needs to be updated by setting its value to the average of the index of the elements before and after. For example:

```
1.0
2.0
3.0
4.0

1.0
3.0
2.0
4.0

1.0
1.5
2.0
4.0
```
This pretty much makes it an O(1) operation since only one value needs to be updated. 

In practice in the frontend it's implemented by checking all elements and updating them only if their index has changed since it's really cumbersome to keep track of what element moved where turning it again into an O(n) operation but what you gonna do? ^_~ 

