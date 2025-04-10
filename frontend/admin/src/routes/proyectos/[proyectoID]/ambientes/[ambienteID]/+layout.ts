import { error } from '@sveltejs/kit';
import graphql from '$lib/utilities/api';

export const load = async ({ params, fetch }) => {
    const spaceID: number = +params.ambienteID;

    if (Number.isNaN(spaceID)) error(404, `Ambiente con ID ${spaceID} no existe.`);

    const query = `
            query getSpace($id: Int!) {
                space(id: $id) {
                    id
                }
            }
        `;

    const variables = { id: spaceID };

    const ambienteData = (await graphql(query, variables, fetch)).space;

    if (!ambienteData) error(404, `Ambiente con ID ${spaceID} no existe.`);
}
