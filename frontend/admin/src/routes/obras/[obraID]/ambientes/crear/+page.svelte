<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import { yup } from 'sveltekit-superforms/adapters';
	import { spaceCreateSchema } from '$lib/utilities/yupSchemas';
	import TextInput from '$lib/components/input/TextInput.svelte';
	import Markdown from '$lib/components/markdown/Markdown.svelte';
	import type { PageData } from './$types';
	import { PUBLIC_graphql } from '$env/static/public';
	import { goto } from '$app/navigation';
	import { error } from '$lib/utilities/toasts';

	const { data }: { data: PageData } = $props();
	let submitting: boolean = $state(false);

	const { form, errors, enhance } = superForm(data.createForm, {
		SPA: true,
		resetForm: false,
		validators: yup(spaceCreateSchema),
		async onUpdate({ form }) {
			if (form.valid) {
				const query = `
					mutation newSpace($projectId: Int!, $name: String!, $description: String) {
						createSpace(projectId: $projectId, name: $name, description: $description) {
							__typename
							... on ProjectNotFoundSpace {
								projectId
							}
							... on Space {
								name
								description
							}
						}
					}
				`;

				const variables = { projectId: Number.parseInt(data.projectId), ...form.data };

				const res = await fetch(PUBLIC_graphql, {
					method: 'POST',
					body: JSON.stringify({ query, variables }),
					credentials: 'include',
					headers: {
						'Content-Type': 'application/json'
					}
				});

				if (res.ok) {
					const projectData = (await res.json()).data.createSpace;

					switch (projectData.__typename) {
						case 'ProjectNotFoundSpace':
							error(`Proyecto con ID ${projectData.obraId} no existe.`);
						case 'Space':
							await goto(`/obras/${data.projectId}`);
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
