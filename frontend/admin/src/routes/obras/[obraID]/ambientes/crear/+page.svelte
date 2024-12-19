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
	import { error } from '$lib/utilities/toasts';

	const { data }: { data: PageData } = $props();
	let submitting: boolean = $state(false);

	const { form, errors, enhance } = superForm(data.createForm, {
		SPA: true,
		resetForm: false,
		validators: yup(ambienteCreateSchema),
		async onUpdate({ form }) {
			if (form.valid) {
				const query = `
					mutation newAmbiente($obraId: Int!, $name: String!, $description: String) {
						createAmbiente(obraId: $obraId, name: $name, description: $description) {
							__typename
							... on ObraNotFoundAmbiente {
								obraId
							}
							... on Ambiente {
								name
								description
							}
						}
					}
				`;

				const variables = { obraId: Number.parseInt(data.obraID), ...form.data };

				const res = await fetch(PUBLIC_apiUrl, {
					method: 'POST',
					body: JSON.stringify({ query, variables }),
					credentials: 'include',
					headers: {
						'Content-Type': 'application/json'
					}
				});

				if (res.ok) {
					const ambienteData = (await res.json()).data.createAmbiente;

					switch (ambienteData.__typename) {
						case 'ObraNotFoundAmbiente':
							error(`Obra con ID ${ambienteData.obraId} no existe.`);
						case 'Ambiente':
							await goto(`/obras/${data.obraID}`);
							break;
					}
				} else throw res.status;
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
