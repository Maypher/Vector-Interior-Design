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
					mutation createProject($name: String!, $descriptionEs: String!, $descriptionEn: String!, $area: Int!) {
						createProject(name: $name, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn, area: $area) {
							id
						}
					}
				`;
				const variables = { ...form.data };

				const newProjectId = (await graphql(query, variables)).createProject.id;

				await goto(`/proyectos/${newProjectId}`);
			}

			submitting = false;
		}
	});

	let submitting: boolean = $state(false);
	let english: boolean = $state(false);
</script>

<div class="flex justify-center items-center h-full">
	<form class="p-4 m-5 bg-gray-700" use:enhance>
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
			<div class="my-4">
				<input type="checkbox" id="language" hidden bind:checked={english} />
				<label
					for="language"
					class="bg-vector-orange hover:cursor-pointer hover:brightness-75 p-1 border-vector-black border-2 transition-colors"
				>
					{english ? 'Ingles' : 'Español'}
				</label>
				{#if english}
					<Markdown
						label="Descripción"
						name="description"
						bind:value={$form.descriptionEn}
						errors={$errors.descriptionEn}
						{...$constraints.descriptionEn}
					/>
				{:else}
					<Markdown
						label="Descripción"
						name="description"
						bind:value={$form.descriptionEs}
						errors={$errors.descriptionEs}
						{...$constraints.descriptionEs}
					/>
				{/if}
			</div>
			<button type="submit" class="bg-blue-400 rounded-md m-2 p-2">Crear Proyecto</button>
		</fieldset>
	</form>
</div>
