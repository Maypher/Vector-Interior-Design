import i18next from "i18next";
import { createI18nStore } from "svelte-i18next";
import type { i18n } from "i18next";
import { type Writable } from "svelte/store";
import { setContext, getContext } from "svelte";

i18next.init({
    lng: 'en',
    resources: {
        en: {
            translation: {
                "key": "hello world"
            }
        }
    },
    interpolation: {
        escapeValue: false, // not needed for svelte as it escapes by default
    }
});

export default () => createI18nStore(i18next);

const key = 'i18n';

export function setI18n(ctx: Writable<i18n>) { setContext(key, ctx); }
export function getI18n(): Writable<i18n> { return getContext(key); }
