<script lang="ts">
	import { yup } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types';
	import { superForm } from 'sveltekit-superforms';
	import { ambienteCreateSchema } from '$lib/utilities/yupSchemas';
	import EditableInput from '$lib/components/input/EditableInput.svelte';
	import Markdown from '$lib/components/markdown/Markdown.svelte';
	import { success } from '$lib/utilities/toasts';
	import graphql from '$lib/utilities/api';
	import confirmationDialog from '$lib/utilities/dialog';
	import { goto } from '$app/navigation';
	import { error } from '@sveltejs/kit';

	const { data }: { data: PageData } = $props();
	let ambiente = $state(data.ambienteData);
	let submitting: boolean = $state(false);

	const { form, errors, enhance, constraints } = superForm(data.updateForm, {
		SPA: true,
		validators: yup(ambienteCreateSchema),
		resetForm: false,
		invalidateAll: false,
		async onUpdate({ form: updateForm }) {
			submitting = true;
			if (updateForm.valid) {
				const query = `
                    mutation UpdateAmbiente($id: Int!, $name: String, $description: String) {
                        updateAmbiente(id: $id, name: $name, description: $description) {
                            name
                            description
                        }
                    }
                `;

				const variables = { id: ambiente.id, ...updateForm.data };

				const updatedAmbiente = (await graphql(query, variables)).updateAmbiente;
				$form.name = updatedAmbiente.name;
				$form.description = updatedAmbiente.description;

				success(`Ambiente "${updatedAmbiente.name}" actualizado con éxito.`);
			}
			submitting = false;
		}
	});

	async function deleteAmbiente() {
		if (
			await confirmationDialog(
				`Seguro que quieres borrar el ambiente <b>${ambiente.name}</b> 
				de la obra <b>${data.ambienteData.obra.name}</b>? 
				Esta acción no puede ser revertida.`
			)
		) {
			const query = `
				mutation deleteAmbiente($id: Int!) {
					deleteAmbiente(id: $id) {
						name
					}
				}
			`;

			const variables = { id: ambiente.id };

			const deletedAmbiente = (await graphql(query, variables)).deleteAmbiente;

			if (deletedAmbiente) {
				await goto(`/obras/${data.ambienteData.obra.id}/`);
			} else error(404, `Ambiente con ID ${ambiente.id} no existe.`);
		}
	}
</script>

<div class="w-full bg-green-300 min-h-screen p-3">
	<form action="POST" use:enhance class="max-w-xl p-3 rounded-md m-auto bg-red-700">
		<fieldset disabled={submitting}>
			<button
				type="button"
				class="block w-fit ml-auto p-2 rounded-sm bg-blue-600 hover:bg-amber-600"
				onclick={deleteAmbiente}>Eliminar</button
			>
			<EditableInput
				name="nombre"
				label="Nombre"
				type="text"
				bind:value={$form.name}
				errors={$errors.name}
				{...$constraints.name}
			/>
			<Markdown
				label="Descripción"
				name="descripcion"
				bind:value={$form.description}
				errors={$errors.description}
			/>
			<button type="submit" class="bg-violet-300 hover:bg-stone-50 m-2 rounded-sm p-3"
				>Actualizar</button
			>
		</fieldset>
	</form>
	<hr class="m-2 border-blue-700" />
	<div class="m-2">
		<h1 class="text-xl text-center">Imágenes</h1>
		<ul class="w-fit mx-auto my-2">
			{#each ambiente.images as image}
				<li class="size-48">
					<a
						href={`/obras/${data.ambienteData.obra.id}/ambientes/${ambiente.id}/imagenes/${image.filename}`}
					>
						<img src={`http://localhost:8080/images/${image.filename}`} alt={ambiente.altText} />
					</a>
				</li>
			{/each}
		</ul>
		<a
			href={`/obras/${data.ambienteData.obra.id}/ambientes/${ambiente.id}/imagenes/crear/`}
			class="block w-fit m-auto bg-amber-400 hover:bg-white p-2 rounded-md">Nueva imagen</a
		>
	</div>
</div>
