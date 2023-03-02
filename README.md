# Getting Started with this project

1. Clone the repository, initialize submodule and pull submodule

`git clone --recurse-submodule https://github.com/urban-toolkit/urbantk-react-ts.git`
 
2. Virtual environment  

Tested Python version '3.10.6'  

- The easiest way to install all dependencies is by using an [anaconda](https://www.anaconda.com/) virtual environment
- After installing anaconda run:
- `conda create -n urbantk -c conda-forge --file conda-package-list.txt`
- `conda activate urbantk`
- go to urbantk-react-ts
- run `pip install -r requirements_pip.txt` (python scripts requirements)
- To load data from pbf it is necessary to be in a windows environment and activate wsl. In the wsl cmd run `apt get install osmium-tool`

3. Backend configuration 

   - go to urbantk-react-ts/src/urbantk-map/
   - git checkout main
   - git pull origin main
   - cd ts
   - run `npm install`
   - run `npm run build`

4. Frontend configuration
   - go back to urbantk-react-ts folder
   - run `npm install --force`
   - to see web version `npm run start:web`
   - to see the VR version `npm run start:vr`
   - to see the CAVE2 version `npm run start:cave`

5. Cuda Installation (for shadow ray tracing)

   - a CUDA-enabled GPU with compute capability 5.0 (Maxwell) to latest (Ampere);
       - NVIDIA driver >= r515;
   - Python 3 64-bit
   - Windows:
       - Framework .NET >= 4.8 (present in all modern Windows)
   - Linux:
       - Mono Common Language Runtime >= 6.6
       - pythonnet
       - FFmpeg >= 4.1

- https://developer.nvidia.com/cuda-downloads



### Configuration

All important configuration parameters are situated in src/params.js or src/pythonServerConfig.json.  

### Info

Web runs on the 3000 port. VR and CAVE2 runs in the 3001 port.  

When specifying the layers buildings has allways to be the last one.  

The name of the layer file must be equal to the id of the layer.

### Available start options

- "start:web": Starts the web version
- "build:web": Builds the bundle for web version (broken)
- "start:vr": Starts the VR version
- "build:vr": Builds the bundle for the VR version (broken)
- "start:cave": Starts the CAVE2 version
- "start:cave:local": Starts the CAVE2 version locally (for testing purposes) (not implemented)
- "build": Build web version and bundle (broken)
- "build:bundle": Build webpack bundle
- "test": Run tests (not implemented)

### About the data

The data used in the stages is served through the public folder.  

If one wants to change which data is being loaded the paramsMapView.environmentDataFolder has to be changed inside src/params.js 

Obs: Currently it is only possible to load public/data/example_mesh_nyc, because it is the only example that uses the projection 3395 instead of lat/lng.

### To load project into the CAVE2

### Package List

1. react-bootstrap - https://www.npmjs.com/package/react-bootstrap
2. react-draggable - https://www.npmjs.com/package/react-draggable
3. d3 - https://www.npmjs.com/package/d3
4. @types/d3 - https://www.npmjs.com/package/@types/d3
5. react-icons - https://www.npmjs.com/package/react-icons
6. jquery - https://www.npmjs.com/package/jquery
7. @types/jquery - https://www.npmjs.com/package/@types/jquery
8. react-dropdown - https://www.npmjs.com/package/react-dropdown
9. @types/d3-scale - https://www.npmjs.com/package/@types/d3-scale
10. axios - https://www.npmjs.com/package/axios

## creating submodule
git submodule add link_to_the_repository_to_be_added_as_submodule

### submodule cloning
1. clone the repository as usual
2. run - git submodule init
3. run - git submodule update

### to fetch and update submodule
git submodule update --remote submoduleName


### multiple entry points 
https://stackoverflow.com/questions/55308657/create-react-app-v2-multiple-entry-points
https://medium.com/swlh/how-to-add-multiple-entry-points-to-your-react-app-ea8bc015d410

## jupyter bundle creation

1. Go to src/urbantk-map/ts
2. run `npm run build`
3. Paste in the header of src/urbantk-map/ts/dist/urbantkmap.js:  
   /* eslint-disable @typescript-eslint/no-empty-function */  
   /* eslint-disable no-cond-assign */  
   /* eslint-disable require-yield */  
3. In terminal urbantk-react/ run `npm run build:bundle:jupyter`
    it will create a single bundle file in /dist/bundle folder - "bundle.min.js"
    this bundle can be used to render our project in jupyter notebook
4. Go to src/pythonComponents/jupyterSupport run `jupyter notebook`
5. Run the notebook that will open on the web browser

## web bundle creation

1. in terminal run "npm run build:bundle:web"
    it will create a single bundle file in dist/bundle folder that can be used with basic html file
    make sure to run the server in port 3000
    make sure to add the data folder with data
