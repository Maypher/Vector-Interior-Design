<script lang="ts">
	import TextInput from '$lib/components/input/TextInput.svelte';
	import Markdown from '$lib/components/markdown/Markdown.svelte';
	import { obraCreateSchema } from '$lib/utilities/yupSchemas';
	import { goto } from '$app/navigation';
	import { superForm, superValidate } from 'sveltekit-superforms';
	import { yup } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types';
	import { PUBLIC_apiUrl } from '$env/static/public';

	const { data }: { data: PageData } = $props();
	let dialog: HTMLDialogElement | null | undefined = $state();

	const { form, errors, enhance, constraints } = superForm(data.createForm, {
		SPA: true,
		validators: yup(obraCreateSchema),
		resetForm: false,
		async onUpdate({ form }) {
			submitting = true;

			if (form.valid) {
				const query = `
					mutation createObra($name: String!, $description: String!, $area: Int!) {
						createObra(name; $name, description: $description, area: $area) {
							id
						}
					}
				`;

				const variables = { ...form.data };

				const res = await fetch(PUBLIC_apiUrl, {
					method: 'POST',
					body: JSON.stringify({ query, variables }),
					credentials: 'include',
					headers: {
						'Content-Type': 'application/json'
					}
				});

				const newObraId = (await res.json()).data.createObra.id;

				if (res.ok) await goto(`/obras/${newObraId}`);
			}

			submitting = false;
		}
	});

	let submitting: boolean = $state(false);
</script>

<div class="flex justify-center items-center h-full">
	<form class="bg-green-500 p-4 m-5" use:enhance>
		<fieldset disabled={submitting}>
			<TextInput
				type="text"
				label="Nombre"
				name="name"
				bind:value={$form.name}
				errors={$errors.name}
				{...$constraints.name}
			/>
			<TextInput
				type="number"
				label="Área (m²)"
				name="area"
				bind:value={$form.area}
				errors={$errors.area}
				{...$constraints.area}
			/>
			<Markdown
				label="Descripción"
				name="description"
				bind:value={$form.description}
				errors={$errors.description}
				{...$constraints.description}
			/>
			<button type="submit" class="bg-blue-400 rounded-md m-2 p-2">Crear Obra</button>
		</fieldset>
	</form>
</div>
