import { type Obra } from '$lib/utilities/interfaces.js';
import { obraCreateSchema } from '$lib/utilities/yupSchemas.js';
import { error } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { PUBLIC_apiUrl } from '$env/static/public';

export async function load({ params, fetch }) {
    const obraID = params.obraID;

    const res = await fetch(PUBLIC_apiUrl + `/obras/${obraID}`, {
        credentials: "include"
    });

    if (res.ok) {
        let obraData: Obra = await res.json();
        const strippedObra = {
            name: obraData.name,
            area: obraData.area,
            description: obraData.description
        }; // Remove all other values that come with the obra since they mess up server side

        const updateForm = await superValidate(strippedObra, yup(obraCreateSchema));

        return { updateForm, obraData };
    }
    else if (res.status === 404) {
        error(404, `Obra con ID ${obraID} no existe.`);
    }
}
