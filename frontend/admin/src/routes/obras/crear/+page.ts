import { superValidate } from "sveltekit-superforms";
import { obraCreateSchema } from "$lib/utilities/yupSchemas";
import { yup } from "sveltekit-superforms/adapters";

export async function load() {
    const createForm = await superValidate(yup(obraCreateSchema));

    return { createForm };
}
