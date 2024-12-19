<script lang="ts">
	import { yup } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types';
	import { superForm } from 'sveltekit-superforms';
	import { ambienteCreateSchema } from '$lib/utilities/yupSchemas';
	import EditableInput from '$lib/components/input/EditableInput.svelte';
	import Markdown from '$lib/components/markdown/Markdown.svelte';
	import { PUBLIC_apiUrl } from '$env/static/public';
	import { success } from '$lib/utilities/toasts';
	import graphql from '$lib/utilities/api';

	const { data }: { data: PageData } = $props();
	let ambiente = $state(data.ambienteData);
	let submitting: boolean = $state(false);

	const { form, errors, enhance, constraints } = superForm(data.updateForm, {
		SPA: true,
		validators: yup(ambienteCreateSchema),
		resetForm: false,
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
</script>

<div class="w-full bg-green">
	<form action="POST" use:enhance>
		<fieldset disabled={submitting}>
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
			<button type="submit">Actualizar</button>
		</fieldset>
	</form>
	<div>
		{#each ambiente.images as image}
			<a href={`/obras/${data.obraID}/ambientes/${ambiente.id}/imagenes/${image.filename}`}>
				<img src={`http://localhost:8080/images/${image.filename}`} alt={ambiente.altText} />
			</a>
		{/each}
		<a href={`/obras/${data.obraID}/ambientes/${ambiente.id}/imagenes/crear/`}>Nueva imagen</a>
	</div>
</div>
