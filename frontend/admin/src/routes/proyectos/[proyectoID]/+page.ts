import { projectCreateSchema } from '$lib/utilities/yupSchemas.js';
import { error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import graphql from '$lib/utilities/api.js';

export async function load({ params, fetch }) {
    const projectID: number = +params.proyectoID;

    if (Number.isNaN(projectID)) error(404, `Proyecto con ID ${projectID} no existe.`);

    const query = `
                query getProject($id: Int!) {
                    project(id: $id) {
                        id
                        nameEs
                        nameEn
                        descriptionEs
                        descriptionEn
                        area
                        public
                        spaces {
                            id
                            name
                            images {
                                filename
                                imageUrl
                                altTextEs
                                mainPage
                                sculpture
                                space {
                                    project {
                                        thumbnail {
                                            filename
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
           `;
    const variables = { id: projectID };

    const projectData = (await graphql(query, variables, fetch)).project;

    const formData = {
        nameEs: projectData.nameEs,
        nameEn: projectData.nameEn,
        descriptionEs: projectData.descriptionEs,
        descriptionEn: projectData.descriptionEn,
        area: projectData.area
    };
    const updateForm = await superValidate(formData, yup(projectCreateSchema));

    if (projectData) return { updateForm, projectData };
    else error(404, `Proyecto con ID ${projectID} no existe.`);
}
