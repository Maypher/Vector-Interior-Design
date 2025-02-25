<script lang="ts">
	import { getI18n } from '$lib/i18n';
	import { page } from '$app/state';
	import { type Snippet } from 'svelte';
	import cookies from 'js-cookie';
	import type { PageData } from './$types';
	import { afterNavigate } from '$app/navigation';

	let { children, data }: { data: PageData; children: Snippet } = $props();
	const i18n = getI18n();

	afterNavigate(() => {
		const selectedLang = data.selectedLanguage;
		const currentLang = page.url.pathname.split('/').at(1);

		if (currentLang !== selectedLang) {
			const redirectTo = `/${selectedLang}/${getRemainingUrl()}`;
			location.replace(redirectTo);
		}
	});

	async function changeLanguage(lang: string) {
		console.log(getRemainingUrl());
		cookies.set('lang', lang, { path: '/', httpOnly: false });
		const redirectTo = `/${lang}/${getRemainingUrl()}`;
		location.replace(redirectTo);
	}

	function getRemainingUrl(): string {
		// Removing the first element since the url is /en/something and the first element is an empty string
		const splitURL = page.url.pathname.split('/').slice(1);
		const remainingURL = splitURL.slice(1);

		return remainingURL.join('/');
	}
</script>

<div class="absolute right-0 top-0 z-20">
	<select onchange={(e) => changeLanguage((e.target as HTMLSelectElement).value)}>
		<option value="en" selected={$i18n.language === 'en'}>{$i18n.t('english')}</option>
		<option value="es" selected={$i18n.language === 'es'}>{$i18n.t('Spanish')}</option>
	</select>
</div>
{@render children()}
