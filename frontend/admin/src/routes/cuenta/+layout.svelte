<script>
	let { children } = $props();
</script>

<div class="min-h-screen bg-black flex justify-center align-middle items-center">
	{@render children()}
</div>
