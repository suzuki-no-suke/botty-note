<script lang="ts">
    import { WIKI_BACK_URL } from "$lib/constants";
    import { onMount } from "svelte";

    export let data;

    let fileDetail;

    async function get_content(path: string) {
        const response = await fetch(`${WIKI_BACK_URL}/file/detail?filepath=/${path}`);
        if (response.ok) {
            fileDetail = await response.json();
            console.log(fileDetail);
            fileContents = fileDetail.contents;
            editMode = false;
        } else {
            console.error('Failed to fetch file detail data');
        }
    }

    let fileContents = "";

    async function save_content(fullpath: string) {
        const response = await fetch(`${WIKI_BACK_URL}/file/update`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                fullpath: fullpath,
                content_type: null,
                contents: fileContents,
                tags: null
            })
        });
        if (response.ok) {
            const result = await response.json();
            console.log(result);
            if (result.succeed) {
                await get_content(fullpath);
            }
        } else {
            console.error('Failed to update file');
        }
    }

    let editMode = false;

    onMount(() => {
        const path = data.path;
        console.log("path is -> ", path);
        get_content(path);
    });
</script>

<h1>Edit</h1>

{#if fileDetail}
<h3> {fileDetail.name} </h3>
<p> fullpath = {fileDetail.fullpath}</p>

{#if editMode}
<h2>Edit Mode</h2>
<button on:click={() => save_content(fileDetail.fullpath)}>保存</button>

<textarea bind:value={fileContents} rows="80" cols="120"></textarea>

<button on:click={() => save_content(fileDetail.fullpath)}>保存</button>

{:else}
<h2>Viewer Mode</h2>
<button on:click={() => {editMode = true;}}>編集</button>

<pre><code>{fileContents}</code></pre>

<button on:click={() => {editMode = true;}}>編集</button>

{/if}


{:else}
<h3>wait for load file</h3>
{/if}
