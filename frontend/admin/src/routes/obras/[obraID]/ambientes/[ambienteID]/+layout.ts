import { error } from '@sveltejs/kit';
import graphql from '$lib/utilities/api';

export const load = async ({ params, fetch }) => {
    const ambienteID: number = +params.ambienteID;

    if (Number.isNaN(ambienteID)) error(404, `Ambiente con ID ${ambienteID} no existe.`);

    const query = `
            query getAmbiente($id: Int!) {
                ambiente(id: $id) {
                    id
                }
            }
        `;

    const variables = { id: ambienteID };

    const ambienteData = (await graphql(query, variables, fetch)).ambiente;

    if (!ambienteData) error(404, `Ambiente con ID ${ambienteID} no existe.`);
}
