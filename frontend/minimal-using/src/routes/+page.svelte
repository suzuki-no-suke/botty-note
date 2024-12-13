<script lang="ts">
    import { onMount } from "svelte";
    import { WIKI_BACK_URL } from "$lib/constants";
    import FolderTree from "$lib/FolderTree.svelte";
    import { goto } from "$app/navigation";
    import { base } from "$app/paths";

    let treeData;
    let selectedData;

    $: console.log("select update -> ", selectedData);
    $: folder_detail(selectedData);

    onMount(async () => {
        await load_tree();
    });

    async function load_tree() {
        const response = await fetch(`${WIKI_BACK_URL}/tree`);
        if (response.ok) {
            treeData = await response.json();
            console.log(treeData);
        } else {
            console.error('Failed to fetch tree data');
        }
    }

    let folderDetail = null;

    async function folder_detail(path: string) {
        if (!path) {
            console.error('path not specified');
            return;
        }

        const response = await fetch(`${WIKI_BACK_URL}/folder/detail?dirpath=${path}`);
        if (response.ok) {
            folderDetail = await response.json();
            console.log(folderDetail);
        } else {
            console.error('Failed to fetch folder detail data');
        }
    };

    let createFolderMode = false;
    let newFolderName;
    async function create_folder(parent: string, name: string) {
        createFolderMode = false;

        const response = await fetch(`${WIKI_BACK_URL}/folder/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                parent: parent,
                name: name
            })
        });
        if (response.ok) {
            const result = await response.json();
            console.log(result);
            if (result.succeed) {
                newFolderName = "";
                await load_tree();
                await folder_detail(parent);
            }
        } else {
            console.error('Failed to create folder');
        }
    };


    let createFileMode = false;
    let newFileName;
    async function create_file(parent: string, name: string) {
        createFileMode = false;

        const response = await fetch(`${WIKI_BACK_URL}/file/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                parent: parent,
                name: name
            })
        });
        if (response.ok) {
            const result = await response.json();
            console.log(result);
            if (result.succeed) {
                newFileName = "";
                await folder_detail(parent);
            }
        } else {
            console.error('Failed to create file');
        }
    };

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

    function to_edit_page(fullpath: string){
        get_content(fullpath);
    };
</script>


<h1>Botty Note Folder Tree</h1>

{#if treeData && treeData.root_node}
<FolderTree folder={treeData.root_node} bind:selected={selectedData} />
{:else}
<p>now loading...</p>
{/if}

<hr/>


<h2>Folder Detail</h2>

{#if folderDetail}

<h3>fullpath = {folderDetail.fullpath}</h3>

<h3>folders</h3>
<ul>
    {#each folderDetail.children as c}
        <li>{c}</li>
    {/each}
    <li>
        {#if !createFolderMode}
        <button on:click={() => {createFolderMode = true}}>Create new folder</button>
        {:else}
        <span>create : {folderDetail.fullpath} <input bind:value={newFolderName}/> / </span>
        <button on:click={() => create_folder(folderDetail.fullpath, newFolderName)}>create folder</button>
        {/if}
    </li>
</ul>


<h3>files</h3>
<ul>
    {#each folderDetail.files as f}
        <li><button on:click={() => to_edit_page(folderDetail.fullpath + f)}>{f}</button></li>
    {/each}
    {#if !createFileMode}
    <button on:click={() => {createFileMode = true}}>Create new file</button>
    {:else}
    <span>create : {folderDetail.fullpath} <input bind:value={newFileName}/> </span>
    <button on:click={() => create_file(folderDetail.fullpath, newFileName)}>create empty file</button>
    {/if}
</ul>


{:else}
<p>please select folder</p>
{/if}


<hr/>

<h3>File Detail</h3>
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



<style lang="postcss">
    :global(button) {
        @apply border p-1;
    }

    :global(textarea) {
        @apply border dark:border-gray-600;
        @apply font-mono text-sm;
    }
</style>