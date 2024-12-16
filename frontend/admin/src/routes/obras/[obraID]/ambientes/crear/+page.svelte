<script lang="ts">
	import type { Ambiente } from '$lib/utilities/interfaces';
	import { superForm, defaults } from 'sveltekit-superforms';
	import { yup } from 'sveltekit-superforms/adapters';
	import { ambienteCreateSchema } from '$lib/utilities/yupSchemas';
	import objectToFormData from '$lib/utilities/formData';
	import TextInput from '$lib/components/input/TextInput.svelte';
	import Markdown from '$lib/components/markdown/Markdown.svelte';
	import type { PageData } from './$types';
	import { PUBLIC_apiUrl } from '$env/static/public';
	import { goto } from '$app/navigation';

	const { data }: { data: PageData } = $props();
	let submitting: boolean = $state(false);

	const { form, errors, enhance } = superForm(data.createForm, {
		SPA: true,
		validators: yup(ambienteCreateSchema),
		async onUpdate({ form }) {
			if (form.valid) {
				const finalData = { obra_id: data.obraID, ...form.data };
				const formData = objectToFormData(finalData);

				const res = await fetch(PUBLIC_apiUrl + '/ambientes/crear', {
					method: 'POST',
					body: formData,
					credentials: 'include'
				});

				if (res.ok) await goto(`/obras/${data.obraID}`);
				else throw res.status;
			}
		}
	});
</script>

<form method="POST" use:enhance class="max-w-xl bg-orange-600 m-auto my-5 p-3">
	<fieldset disabled={submitting}>
		<TextInput
			name="nombre"
			label="Nombre"
			type="text"
			errors={$errors.name}
			bind:value={$form.name}
		/>
		<Markdown
			name="description"
			label="Descripción"
			errors={$errors.description}
			bind:value={$form.description}
		/>
		<button class="bg-purple-700 rounded-sm p-3 m-2">Crear</button>
	</fieldset>
</form>
