<script lang="ts">
	interface Errors {
		errors: Array<string>;
	}

	let { errors }: Errors = $props();
</script>

<div class="text-red-600">
	{#if errors}
		{errors.join(' ')}
	{/if}
</div>
