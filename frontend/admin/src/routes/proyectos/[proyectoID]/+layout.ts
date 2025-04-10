import graphql from "$lib/utilities/api";
import { error } from "@sveltejs/kit";

export async function load({ params, fetch }) {
    const projectID: number = +params.proyectoID;

    if (isNaN(projectID)) error(404, `Proyecto con ID ${projectID} no existe.`);


    const query = `
                    query getProject($id: Int!) {
                        project(id: $id) {
                            id
                        }
                    }
               `;
    const variables = { id: projectID };

    const projectData = (await graphql(query, variables, fetch)).project;

    if (!projectData) error(404, `Proyecto con ID ${projectID} no existe.`);
}
