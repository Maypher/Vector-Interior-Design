<script lang="ts">
	import EditableInput from '$lib/components/input/EditableInput.svelte';
	import Markdown from '$lib/components/input/Markdown.svelte';

	const { data } = $props();

	let updateObra = $state(data);
</script>

<div class="bg-green-700 h-screen">
	<form action="POST" class="bg-purple-900 m-auto p-4">
		<EditableInput
			name="name"
			label="Nombre"
			bind:value={updateObra.name}
			errors={[]}
			type="text"
		/>
		<Markdown />
	</form>
</div>
