<script lang="ts">
	import Errors from './Errors.svelte';

	interface props {
		label: string;
		name: string;
		type: 'text' | 'number';
		value: string;
		errors: Array<string>;
	}

	let { label, name, type, value = $bindable(''), errors }: props = $props();
</script>

<div class="my-2 flex-col">
	<label for={name} class="block text-md">{label}</label>
	<input {type} {name} class="p-1 rounded-md w-full focus:outline-none" bind:value />
	<Errors {errors} />
</div>
