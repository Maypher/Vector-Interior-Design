<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import { yup } from 'sveltekit-superforms/adapters';
	import { spaceCreateSchema } from '$lib/utilities/yupSchemas';
	import type { PageData } from './$types';
	import graphql from '$lib/utilities/api';
	import { goto } from '$app/navigation';
	import { error } from '$lib/utilities/toasts';

	const { data }: { data: PageData } = $props();
	const project = data.project;
	let submitting: boolean = $state(false);

	const { form, errors, enhance } = superForm(data.createForm, {
		SPA: true,
		resetForm: false,
		validators: yup(spaceCreateSchema),
		async onUpdate({ form }) {
			if (form.valid) {
				const query = `
					mutation newSpace($projectId: Int!, $name: String!) {
						createSpace(projectId: $projectId, name: $name) {
							__typename
							... on ProjectNotFoundSpace {
								projectId
							}
							... on Space {
								name
							}
						}
					}
				`;

				const variables = { projectId: Number.parseInt(data.projectId), ...form.data };

				const projectData = (await graphql(query, variables)).createSpace;

				switch (projectData.__typename) {
					case 'ProjectNotFoundSpace':
						error(`Proyecto con ID ${projectData.projectId} no existe.`);
					case 'Space':
						await goto(`/proyectos/${data.projectId}`);
						break;
				}
			}
		}
	});
</script>

<div class="bg-black h-[calc(100svh-5rem)] flex items-center">
	<form
		method="POST"
		use:enhance
		class="max-w-xl w-full bg-gray-700 backdrop-brightness-75 m-auto p-5"
	>
		<h1 class="text-xl text-center text-white">
			Crear ambiente para <a href={`/proyectos/${project.id}`} class="border-b-2 border-vector-grey"
				>{project.nameEs}</a
			>
		</h1>
		<fieldset disabled={submitting}>
			<div class="w-full my-10 flex flex-col gap-2">
				<label for="name" class="block text-white">Nombre</label>
				<input type="text" bind:value={$form.name} class="bg-white w-full p-2" />
			</div>
			<button
				class="bg-vector-orange transition-colors hover:brightness-125 cursor-pointer rounded-md p-3 m-2 disabled:brightness-75 disabled:cursor-not-allowed"
				disabled={!$form.name}
				>Crear
			</button>
		</fieldset>
	</form>
</div>
