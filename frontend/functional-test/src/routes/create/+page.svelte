<script lang="ts">
    import { onMount } from 'svelte';

    let treeData;

    onMount(async () => {
        const response = await fetch('http://localhost:8000/tree');
        if (response.ok) {
            treeData = await response.json();
            console.log(treeData);
        } else {
            console.error('Failed to fetch tree data');
        }
    });

    let folderDetail;

    async function folder_detail(path: string) {
        const response = await fetch(`http://localhost:8000/folder/detail?dirpath=${path}`);
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

        const response = await fetch("http://localhost:8000/folder/create", {
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

        const response = await fetch("http://localhost:8000/file/create", {
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
                await folder_detail(parent);
            }
        } else {
            console.error('Failed to create file');
        }
    }
</script>

<h2>list all folders</h2>

{#if treeData && treeData.all_folders}
    <ul>
        {#each Object.values(treeData.all_folders) as f}
            <li><button on:click={() => folder_detail(f.fullpath)}>({f.name} / file: {f.num_files}) - {f.fullpath}</button></li>
        {/each}
    </ul>
{/if}

<hr/>

<h2>Folder Detail</h2>

{#if folderDetail}

<h3>fullpath</h3>
<p>{folderDetail.fullpath}</p>

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
        <li>{f}</li>
    {/each}
    {#if !createFileMode}
    <button on:click={() => {createFileMode = true}}>Create new file</button>
    {:else}
    <span>create : {folderDetail.fullpath} <input bind:value={newFileName}/> </span>
    <button on:click={() => create_file(folderDetail.fullpath, newFileName)}>create empty file</button>
    {/if}
</ul>

{:else}
<h3>wait for ready... dir</h3>
{/if}

