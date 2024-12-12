import { type Obra } from '$lib/utilities/interfaces.js';
import { error } from '@sveltejs/kit';

export async function load({ params, fetch }) {
    const obraID = params.id;

    const res = await fetch(`/api/obras/${obraID}`);

    if (res.ok) {
        let data: Obra = await res.json();

        return data;
    }
    else if (res.status === 404) {
        error(404, `Obra con ID ${obraID} no existe.`);
    }
}
