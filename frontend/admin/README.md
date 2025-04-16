# Admin Frontend

This is admin frontend for the Vector: Interior Design website. It is written in sveltekit and it interfaces with the admin backend. Most people won't see or be able to access this site since it's purpose is to setup and configure the user frontend.

It consists of panels to edit project and image data such as description, alt text, and names. It also consists of 3 editors that correspond to the visual aspect of the main page, project page, and sculptures page, all with a desktop and mobile version.

# Routes

- `/cuenta`: Path to the login form. It works by sending an email and password in a form and if validated an http-only cookie is generated with a session id. All other paths are blocked if not logged in.

- `/proyectos`: Path to a list of all projects. From here you can access, reorder, or create new projects through `/proyectos/crear`.
- `/proyectos/esculturas`: Sculptures editor. From here you can change the order of sculptures, add description and change background color.
- `/proyectos/paginaPrincipal`: The editors for the main page. Either redirects to `/movil` or `/escritorio` for the mobile or desktop editor respectively.
- `/proyectos/<project-id>`: The configuration for a specific project. Here you can change the name, description, reorder the images of a project and publish or privatize a project.
- `/proyectos/<project-id>/ambientes/crear`: Creates a new ambient in the project. These are used for organizational purposes only since in the user frontend they aren't hinted at whatsoever.
- `/proyectos/<project-id>/ambientes/<ambient-id>/imagenes/crear`: Creates a new image for the given ambient of the given project.
- `/proyectos/<project-id>/ambientes/<ambient-id>/<filename>`: Page to edit a given image. Here you can change an image's description, it's alt text, set is as the project's thumbnail, put it in the main page, mark it as a sculpture, or hide it from the project view.
- `/proyectos/<project-id>/escritorio`: The desktop editor of the project.
- `/proyectos/<project-id>/movil`: The mobile editor of the project.
