import { error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { imageUpdateSchema } from '$lib/utilities/yupSchemas.js';
import graphql from '$lib/utilities/api.js';

export const load = async ({ fetch, params }) => {
    const filename = params.filename;
    const ambienteId: number = +params.ambienteID;
    const projectId: number = +params.obraID;

    const query = `
        query GetImage($filename: String!) {
            image(filename: $filename) {
                filename
                altText
                description
                descriptionFont
                sculpture
                hideInProject
                mainPage
                space {
                    project {
                        thumbnail {
                            filename
                        }
                    }
                }
                phoneConfig {
                    borders {
                        n
                        s
                        e
                        w
                    }
                    alignment
                    descriptionPos
                    descriptionAlignment
                }
            }
        }
    `;
    const variables = { filename: filename };


    const imageData = (await graphql(query, variables, fetch)).image;

    if (!imageData) error(404, `Imagen ${filename} no existe.`);
    else {
        const updateForm = await superValidate({
            altText: imageData.altText, description: imageData.description || "",
            descriptionFont: imageData.descriptionFont,
            hideInProject: imageData.hideInProject,
            sculpture: imageData.sculpture,
        }, yup(imageUpdateSchema));

        return { imageData, updateForm, ambienteId, projectId }
    };
};
