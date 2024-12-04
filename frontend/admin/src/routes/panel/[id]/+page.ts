import { type ObraData } from '$lib/utilities/interfaces.js';
import { redirectWithToast } from '$lib/utilities/toasts.js';

export async function load({ params, fetch }) {
    const obraID = params.id;

    const res = await fetch(`/api/obras/${obraID}`);

    if (res.ok) {
        let data: ObraData = await res.json();

        return data;
    }

    redirectWithToast("/panel", `No existe la obra con el id ${obraID}.`, "ERROR");
}
