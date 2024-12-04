<script lang="ts">
	import Errors from './Errors.svelte';

	interface props {
		label: string;
		name: string;
		value: string;
		type: string;
		errors: Array<string>;
	}

	let input: HTMLInputElement;

	function onfocusout() {
		input.disabled = true;
		input.classList.add('text-gray-400');
	}

	function enableInput() {
		const end = input.value.length;
		input.setSelectionRange(end, end);
		input.disabled = false;
		input.focus();
		input.classList.remove('text-gray-400');
	}

	let { label, name, value = $bindable(''), type, errors }: props = $props();
</script>

<div class="my-2 flex flex-col">
	<label for={name} class="block my-2">{label}</label>
	<div class="flex bg-white p-1 rounded-md w-fit">
		<input
			{type}
			{name}
			{value}
			bind:this={input}
			class="focus:outline-none text-gray-400"
			{onfocusout}
			disabled
		/>
		<button
			class="material-symbols-outlined size-min pl-2 border-l-2"
			onclick={enableInput}
			type="button"
		>
			edit
		</button>
	</div>
	<Errors {errors} />
</div>
