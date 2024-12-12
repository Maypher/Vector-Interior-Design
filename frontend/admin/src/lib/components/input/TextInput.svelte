<script lang="ts">
	import Errors from './Errors.svelte';

	interface Props {
		label: string;
		name: string;
		type: 'text' | 'number';
		value?: string | number;
		errors: Array<string> | undefined;
	}

	let {
		label,
		name,
		type,
		value = $bindable(type == 'text' ? '' : 1),
		errors,
		...constrains
	}: Props = $props();
</script>

<div class="my-2 flex-col">
	<label for={name} class="block text-md mx-2 my-1">{label}</label>
	<input
		{type}
		{name}
		class="p-1 rounded-md w-full focus:outline-none"
		bind:value
		{...constrains}
	/>
	{#if errors}<Errors {errors} />{/if}
</div>
