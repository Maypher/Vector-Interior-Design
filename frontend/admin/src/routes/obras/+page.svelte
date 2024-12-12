<script lang="ts">
	import { type Obra } from '$lib/utilities/interfaces';

	let searchParams = $state({
		name: '',
		page: 1
	});

	// Used to highlight the search string in the results. Not derived because it should only update on search.
	let nameRegex: RegExp = $state(new RegExp(`(${searchParams.name})`, 'gi'));

	let obraPromise: Promise<Array<Obra>> = $state(fetchObras());

	async function fetchObras() {
		nameRegex = new RegExp(`(${searchParams.name})`, 'gi');

		let queryParams = new URLSearchParams({
			...searchParams,
			page: searchParams.page.toString()
		}).toString();

		const res = await fetch(`/api/obras/?${queryParams}`);

		if (res.ok) {
			const data = await res.json();
			console.log(data);
			console.log(data.obras);
			return data.obras;
		}
	}

	function onclick() {
		obraPromise = fetchObras();
	}
</script>

<div class="bg-red-400 min-h-screen p-4">
	<div class="bg-gray-500 p-2 flex justify-between items-center rounded-lg max-w-md m-auto">
		<input type="text" class="bg-transparent outline-none w-full" bind:value={searchParams.name} />
		<button class="material-symbols-outlined border-l-2 border-gray-700 pl-3" {onclick}>
			search
		</button>
	</div>
	<div class="my-4 max-w-md m-auto">
		{#await obraPromise}
			<p>Cargando...</p>
		{:then data: Array<Obra>}
			<ul class="list-disc">
				{#if data.length == 0}
					{`Ninguna obra con el nombre ${searchParams.name}`}
				{:else}
					{#each data as obra}
						<li>
							<a href={`/panel/${obra.id}`}>
								{@html obra.name.replace(nameRegex, '<b>$1</b>')}
							</a>
							{#if obra.thumbnail}<img
									src={`/images/${obra.thumbnail.filename}`}
									alt={obra.thumbnail.alt_text}
								/>
							{/if}
						</li>
					{/each}
				{/if}
			</ul>
		{/await}
		<a href="/obras/crear">Nueva Obra</a>
	</div>
</div>
