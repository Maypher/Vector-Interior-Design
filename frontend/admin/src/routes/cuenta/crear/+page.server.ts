import { loginSchema } from '$lib/utilities/yupSchemas';
import { fail, redirect } from '@sveltejs/kit';
import { superValidate } from "sveltekit-superforms";
import { yup } from 'sveltekit-superforms/adapters';

export const actions = {
    default: async ({ request }) => {
        const form = await superValidate(request, yup(loginSchema));

        if (!form.valid) {
            return fail(400, { form });
        }

        const res = await fetch("/api/auth/iniciar-sesion", {
            body: await request.formData()
        });

        if (res.ok) redirect(302, "/obras/");
        else {
            const errMsg = await res.text();
            return fail(res.status, { form, errMsg });
        }
    }
}
