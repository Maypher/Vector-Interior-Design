<script lang="ts">
	import Errors from './Errors.svelte';

	interface props {
		label: string;
		name: string;
		value: string | number;
		type: 'text' | 'number';
		errors: Array<string> | undefined;
	}

	let input: HTMLInputElement;

	function onfocusout() {
		input.classList.add('text-gray-400');
		input.disabled = true;
	}

	function enableInput() {
		input.disabled = false;
		const end = input.value.length;
		if (type === 'text') input.setSelectionRange(end, end);
		input.focus();
		input.classList.remove('text-gray-400');
	}

	let {
		label,
		name,
		type,
		value = $bindable(type === 'text' ? '' : 1),
		errors,
		...constrains
	}: props = $props();
</script>

<div class="my-2 flex flex-col">
	<label for={name} class="block my-2">{label}</label>
	<div class="flex bg-white p-1 rounded-md w-fit">
		<input
			{type}
			{name}
			bind:value
			bind:this={input}
			class="focus:outline-none text-gray-400"
			{onfocusout}
			disabled
			{...constrains}
		/>
		<button
			class="material-symbols-outlined size-min pl-2 border-l-2"
			onclick={enableInput}
			type="button"
		>
			edit
		</button>
	</div>
	{#if errors}<Errors {errors} />{/if}
</div>
