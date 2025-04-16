# User frontend

This is the user frontend of the Vector: Interior Design website and it's the site most people will see. It is written in Sveltekit.

# Routes

All routes are nested under `/<lang>/<route>` which allows the site to be displayed in multiple languages. This language is first determined by the `Accept-Language` header but can be changed manually which sets a cookie. Currently available languages are English and Spanish.

- `/`: The main page. It includes all images marked as main page in the admin panel.
- `/sitemap.xml`: The sitemap of the site.
- `/esculturas`: Includes all the images marked as sculptures.
- `/proyectos`: Displays a list of all public projects.
- `/proyectos/<project-id>`: Displays all images of a project.
- `proyectos/conclusion`: A conclusion message shown after the last project.

# Quirks

- During site setup if the main page, projects, or project-id endpoints return an empty list a 403 error is raised indicating that the site is not yet setup showing an under construction page.

- In sculptures for two images to be grouped they both need to be marked as sculptures and be grouped in the project page. The description and background image are taken from the last image so the first one has no effect on the visuals.

- In projects image grouping works the following way: The entire list of images is traversed. When an image marked as group is found it will keep going until it either finds an image with no group or marked as `groupEnd`. This will be considered a group and the images will be put side by side.
