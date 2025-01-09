<script lang="ts">
	import TextInput from '$lib/components/input/TextInput.svelte';
	import Markdown from '$lib/components/markdown/Markdown.svelte';
	import { projectCreateSchema } from '$lib/utilities/yupSchemas';
	import { goto } from '$app/navigation';
	import { superForm, superValidate } from 'sveltekit-superforms';
	import { yup } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types';
	import graphql from '$lib/utilities/api';

	const { data }: { data: PageData } = $props();

	const { form, errors, enhance, constraints } = superForm(data.createForm, {
		SPA: true,
		validators: yup(projectCreateSchema),
		resetForm: false,
		async onUpdate({ form }) {
			submitting = true;

			if (form.valid) {
				const query = `
					mutation createProject($name: String!, $description: String!, $area: Int!) {
						createProject(name: $name, description: $description, area: $area) {
							id
						}
					}
				`;
				const variables = { ...form.data };

				const newProjectId = (await graphql(query, variables)).createProject.id;

				await goto(`/obras/${newProjectId}`);
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
