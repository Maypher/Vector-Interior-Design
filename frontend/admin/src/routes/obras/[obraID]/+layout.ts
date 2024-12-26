import graphql from "$lib/utilities/api";
import { error } from "@sveltejs/kit";

export async function load({ params, fetch }) {
    const obraID: number = +params.obraID;

    if (isNaN(obraID)) error(404, `Obra con ID ${obraID} no existe.`);


    const query = `
                    query GetObra($id: Int!) {
                        obra(id: $id) {
                            id
                        }
                    }
               `;
    const variables = { id: obraID };

    const obraData = (await graphql(query, variables, fetch)).obra;

    if (!obraData) error(404, `Obra con ID ${obraID} no existe.`);
}
