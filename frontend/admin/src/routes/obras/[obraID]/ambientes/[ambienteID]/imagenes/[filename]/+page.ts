import { PUBLIC_apiUrl } from '$env/static/public';
import { error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { imageUpdateSchema } from '$lib/utilities/yupSchemas.js';

export const load = async ({ fetch, params }) => {
    const filename = params.filename;

    const query = `
        query GetImage($filename: String!) {
            image(filename: $filename) {
                filename
                altText
            }
        }
    `;

    const variables = { filename: filename };

    const res = await fetch(PUBLIC_apiUrl, {
        method: "POST",
        body: JSON.stringify({ query, variables }),
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        }
    })

    if (res.ok) {
        const imageData = (await res.json()).data.image;

        if (!imageData) error(404, `Imagen ${filename} no existe.`);
        else {
            const updateForm = await superValidate({ altText: imageData.altText }, yup(imageUpdateSchema));

            return { imageData, updateForm }
        };
    }
};
