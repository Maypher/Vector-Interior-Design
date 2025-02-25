<script lang="ts">
	import { page } from '$app/state';
</script>

<div class="flex h-screen w-screen flex-col items-center justify-center gap-5 text-4xl text-white">
	<h1 class="font-Noopla text-vector-orange text-[20rem]" style="line-height: 0.8;">X</h1>
	<a href="/proyectos" class="font-Noopla"><span id="arrow">&lt;-</span> {page.error?.message}</a>
</div>

<style>
	#arrow {
		position: relative;
		animation: move 1s ease-in-out infinite both;
	}

	@keyframes move {
		0% {
			right: 0;
		}
		50% {
			right: 2%;
		}
		100% {
			right: 0;
		}
	}
</style>
