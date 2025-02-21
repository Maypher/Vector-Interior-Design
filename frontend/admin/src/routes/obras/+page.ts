import graphql from '$lib/utilities/api.js';

export const load = async ({ fetch }) => {
    const query = `
			query getProjects($name: String) {
				projects(name: $name) {
					id
					name
					public
					thumbnail {
						filename
						altText
					}
				}
			}	
		`;
    const projects = (await graphql(query, {}, fetch)).projects;

    return { projects };
}
