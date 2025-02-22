<script lang="ts">
	import logo from '$lib/images/logo.svg';
	import pencil from '$lib/images/pencil.svg';
</script>

<div
	class="bg-vector-grey flex h-screen w-screen flex-col items-center justify-center gap-20 overflow-x-clip p-10"
>
	<a href="/" class="transition-transform hover:scale-110">
		<img src={logo} alt="Vector: Interior Design" class="w-64" />
	</a>
	<div class="flex flex-col items-center gap-20 text-center text-xl">
		<p class="relative z-10 md:whitespace-pre-wrap">
			{`Todo proyecto requiere de un diseño complejo, basado en lineamientos claros y objetivos, sin embargo a la hora 
de crear se pueden romper las reglas manteniendo siempre armonía, ofreciendo exclusividad y mejoras en tu calidad de vida.`}
		</p>
		<p>
			Es por eso que...
			<b class="relative block md:inline">
				Ser diferente tiene sus ventajas <b class="text-vector-orange">.</b>

				<img
					src={pencil}
					alt="pencil"
					class="size-70 rotate-20 absolute bottom-3 right-0 origin-bottom translate-x-1/2"
				/>
			</b>
		</p>
	</div>
</div>

<style>
</style>
