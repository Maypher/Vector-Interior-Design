<script lang="ts">
	import EditableInput from '$lib/components/input/EditableInput.svelte';
	import Markdown from '$lib/components/markdown/Markdown.svelte';
	import { yup } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types';
	import { superForm } from 'sveltekit-superforms';
	import { obraCreateSchema } from '$lib/utilities/yupSchemas';
	import { PUBLIC_apiUrl } from '$env/static/public';
	import { success } from '$lib/utilities/toasts';

	const { data }: { data: PageData } = $props();
	let obraData = $state(data.obraData!);
	let submitting: boolean = $state(false);

	const { form, errors, enhance, constraints } = superForm(data.updateForm!, {
		SPA: true,
		validators: yup(obraCreateSchema), // Uses obraCreateScheme since this will only update name, description and area. All others will be dedicated pages.
		async onUpdate({ form: updateForm }) {
			if (updateForm.valid) {
				// TODO: Query obra data for update
				const query = `
					mutation updateObra($id: Int!, $name: String, $description: String, $area: Int) {
						updateObra(id: $id, name: $name, description: $description, area: $area) {
							name
							description
							area
						}
					}
				`;
				const variables = {
					id: data.obraData.id,
					name: updateForm.data.name,
					description: updateForm.data.description,
					area: updateForm.data.area
				};

				const res = await fetch(PUBLIC_apiUrl, {
					method: 'POST',
					body: JSON.stringify({ query, variables }),
					credentials: 'include',
					headers: {
						'Content-type': 'application/json'
					}
				});

				if (res.ok) {
					const updatedObra = (await res.json()).data.updateObra;

					$form.name = updatedObra.name;
					$form.description = updatedObra.description;
					$form.area = updatedObra.area;

					success(`Obra "${updatedObra.name}" actualizada con exito.`);
				}
			}
		}
	});

	async function changeObraStatus() {
		let formData = new FormData();
		formData.append('public', `${!obraData.public}`);
		const res = await fetch(PUBLIC_apiUrl + `/obras/actualizar/${obraData.id}`, {
			method: 'PUT',
			body: formData,
			credentials: 'include'
		});

		if (res.ok) window.location.reload();
		else throw res.status;
	}
</script>

<div class="bg-green-700 h-screen">
	<div>
		<button
			class={`${obraData.public ? 'bg-red-500' : 'bg-blue-500'} p-3 m-3 rounded-md`}
			onclick={changeObraStatus}>{obraData.public ? 'Privatizar' : 'Publicar'}</button
		>
	</div>
	<!-- Name, area and description -->
	<form class="bg-purple-900 m-auto p-4" use:enhance>
		<fieldset disabled={submitting}>
			<EditableInput
				name="name"
				label="Nombre"
				bind:value={$form.name}
				errors={$errors.name}
				type="text"
				{...$constraints.name}
			/>
			<EditableInput
				name="area"
				label="Área (m²)"
				bind:value={$form.area}
				errors={$errors.area}
				type="number"
				{...$constraints.area}
			/>
			<div class="max-w-xl">
				<Markdown
					label="Descripción"
					name="description"
					bind:value={$form.description}
					errors={$errors.description}
					{...$constraints.description}
				/>
			</div>
			<button class="bg-red-400 p-1 m-1 rounded-md">Actualizar</button>
		</fieldset>
	</form>
	<hr class="m-3" />
	<!-- Ambientes -->
	<ul class="m-4">
		{#each obraData.ambientes as ambiente}
			<li><a href={`/obras/${obraData.id}/ambientes/${ambiente.id}`}>{ambiente.name}</a></li>
		{/each}
	</ul>
	<a href={`/obras/${obraData.id}/ambientes/crear/`}>Nuevo</a>
</div>
