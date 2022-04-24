import PIL
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.http import FileResponse
from django.urls import reverse
from NFT_GEN.models import Image, LayersModel, ProjectDesc, ArchivedProject
from .forms import ProjRegistration
from accounts.models import Customer
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from crm1.settings import BASE_DIR
from django.urls import reverse
from utility.nftstorage import NftStorage
from utility.pinata import Pinata


from shutil import make_archive
from wsgiref.util import FileWrapper
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from random import choices
from random import seed
from os import PathLike
from typing import Union
import subprocess

import os
import json
import zipfile
import glob
import shutil
from API_KEYS.keys import keys
from api.views import auser,getuser
from django.contrib.auth.decorators import login_required
#print(keys)

layer_cnt = 1
rand_seed = 345698135
base_uri = "ipfs://"
NFTSTORAGE_API_KEY = keys['NFTSTORAGE']
PINATA_JWT = keys['PINATA']

#project_name= "Test_Pro"

img_file_list = [] 
meta_file_list = []
gen_imgs = {}

user_d = {}

def add_proj(request):
    
    tuser=User.objects.get(username=getuser())
    request.session['user_id'] = tuser.id
    temp = ProjectDesc()
    temp.user = tuser
    temp.proj_name = request.POST.get('projname')
    temp.total = request.POST.get('total')
    temp.proj_desc = request.POST.get('desc')
    temp.save()
    return HttpResponseRedirect(reverse('LayerGet'))

def edit_proj(request, pk):
    
    tuser=User.objects.get(username=getuser())
    request.session['user_id'] = tuser.id
    temp = ProjectDesc.objects.get(id=pk)
    temp.user = tuser
    temp.proj_name = request.POST.get('projname')
    temp.total = request.POST.get('total')
    temp.proj_desc = request.POST.get('desc')
    temp.save()
    return HttpResponseRedirect(reverse('LayerGet'))


def uploadnft(request):

    nstorage = {}
    c = NftStorage(NFTSTORAGE_API_KEY)
    tuser=User.objects.get(username=getuser())
    po_copy = ArchivedProject()
    po = ProjectDesc.objects.get(user=tuser)

    
    proj_name= po.proj_name
    po_copy.proj_name = po.proj_name
    po_copy.proj_desc = po.proj_desc
    po_copy.user = po.user

    # upload images 
    print(img_file_list)
    print(user_d[tuser.id]['img_files'])

    cid = c.upload(img_file_list, 'image/png')
    po.img_hash = cid
    po_copy.img_hash =  po.img_hash 
    nstorage['image_directory_cid'] = cid
    print(nstorage['image_directory_cid'])
    # update Metadata with CID
    update_meta_cid(meta_file_list, cid)
    
    # upload
    print(meta_file_list)
    print(user_d[tuser.id]['meta_files'])

    cid = c.upload(meta_file_list, 'application/json')
    po.meta_hash = cid
    po_copy.meta_hash =  po.img_hash 
    nstorage['metadata_directory_cid'] = cid
    print(nstorage['metadata_directory_cid'])
    
    p = Pinata(PINATA_JWT)
    for k, v in nstorage.items():
        name = proj_name + ' ' + k.split('_')[0]
        p.pin(name, v)

    contract  = getContract()
    contract=contract.replace('_newuri',"'ipfs://"+cid+"'")
    contract=contract.replace('MyToken',proj_name)

   
    context = {

        "contract":contract,
        "ipfs_url":base_uri + cid,
    }

    # po.stats = stats
    # po_copy.stats =  po.stats

    po.save()
    po_copy.save()
    
    return render(request, "output.html", context)


def update_meta_cid(file, cid):
    for i in file:
        with open(i) as f:
             data = json.load(f)
             img_file = data['image'].replace(base_uri, '')
             data['image'] = base_uri + cid + '/' + img_file
        
        with open(i, 'w') as outfile:
            json.dump(data, outfile, indent=4)    



def generate_mint_stats(all_images, mapping):
    stats = {}

    keys = [i.split("-")[1] for i in mapping.keys()]
    values = [i for i in mapping.values()]

    for x in range(0, len(keys)):
        tmp = {}
        for y in range(0, len(values[x])):
            img_c = {values[x][y]: 0}
            tmp.update(img_c)
        stats[keys[x]] = tmp

    for k, v in all_images.items():
        img_key = [i.split("-")[1] for i in v.keys()]
        img_values = [i for i in v.values()]

        for x in range(0, len(img_key)):
            stats[img_key[x]][img_values[x]] += 1

    with open('./mint_stats', 'w') as outfile:
        json.dump(stats, outfile, indent=4)

    json_pretty = json.dumps(stats, sort_keys=True, indent=4)

    return json_pretty




def homeView(request):
    print(request.user,request.user.id)

    #tuser=User.objects.get(username=getuser())
    #print(tuser.id)
    #request.session['user_id'] = tuser.id
    
    return render(request,'index.html')



def setrarity(request,k):
    img_obj = Image.objects.get(id = k)
    img_obj.rarity = request.POST.get('rarity')
    img_obj.save()
    return HttpResponseRedirect(reverse('LayerGet'))


def LayerGet(request):

    tuser=User.objects.get(username=getuser())
    request.session['user_id'] =tuser.id
    layoutDataF = LayersModel.objects.filter(user=tuser)
    imagesObjects = Image.objects.filter(user=tuser)
    print(ProjectDesc.objects.all())
    if not ProjectDesc.objects.all():
        projObjects = {}   
    else:
        projObjects = ProjectDesc.objects.filter(user=tuser)
        
    print(projObjects)
   
    context={'layoutDataV':layoutDataF,'imagesObjects':imagesObjects,'proj':projObjects}
    return render(request,'layout.html',context)


def LayerPost(request):

    global layer_cnt

    tuser=User.objects.get(username=getuser())
    print(tuser.id)
    request.session['user_id'] = tuser.id
    tlayout = request.POST.get('layoutVariable')
    temp = LayersModel()
    temp.user = tuser
    temp.layer_name = str(layer_cnt) +'-'+ tlayout
    temp.save()
    layer_cnt += 1
    return redirect('LayerGet')


def uploadImage(request,pkk):

    tuser=User.objects.get(username=getuser())
    request.session['user_id'] = tuser.id
    
    
    files = request.FILES.getlist('allimages')  
    img_num = len(files)

    tLayer = LayersModel.objects.get(id=pkk)
    #layerPath = BASE_DIR + '/'+ str(tuser.id) + '/images/' + str(tLayer)

    tLayer.img_num = str(img_num)
    tLayer.save()

    index = 1
    for f in files:
        a = Image()
        a.layer = tLayer
        a.user = tuser
        a.image = f
        a.save()
        #a.save(layerPath)
        index+=1
    
    return redirect('LayerGet')

   
def GenerateImg(request):
    tuser=User.objects.get(username=getuser())
    request.session['user_id'] = tuser.id
    layoutDataF = LayersModel.objects.filter(user=tuser)

    po = ProjectDesc.objects.get(user=tuser)

    
    tot = po.total
    proj = po.proj_name
    tot = int(tot)


    global gen_imgs
    global user_d

    td = {}
    user_d[tuser.id] = {}
    
    d = f(BASE_DIR + '/' + str(tuser.id) +'/images')
    td ={}
    for l in layoutDataF:
        imagesObjects = Image.objects.filter(layer=l)
        l = str(l)
        td[l] = []
        
        for i in imagesObjects:
            td[l].append(float(i.rarity))

    images = {}
    for x in range(1, tot+1):
        dup_image_check = True
        image = {}
        seed(x+rand_seed)
        
        # cycle through attributes and check for uniqueness
        counter = 1
        while dup_image_check:
            output = get_random_selection(d,td)
            if len(images) == 0:
                # this is the first NFT. Skip dup check
                dup_image_check = False
            else:
                checker = list(images.values())
                if output in checker:
                    # duplicate - update seed and reselect
                    seed(rand_seed-x-counter)
                    counter += 1
                else:
                    # not a duplicate
                    dup_image_check = False
        
        image[x] = output
        images.update(image)
        
    gen_imgs = images
    user_d[tuser.id]['gen_imgs'] = images
    generate_image_helper(images,proj,str(tuser.id))
    return redirect('LayerGet')


def f(path):

    d ={}
    dirs = sorted([f for f in os.listdir(path) if not f.startswith('.')])
    for i in dirs:
        sub_dir = os.path.join(path, i)
        files = sorted([f for f in os.listdir(sub_dir) if not f.startswith('.')])
        d[i] = [s.replace(".png", "") for s in files]
    return d


def get_random_selection(attributes,rarity):
    temp = {}
    for i in attributes.keys():
        # get values
        values = attributes[i]
        # get rarity weighting
        weights = rarity[i]
        selection = choices(values, weights)
        # add selection
        temp.update({i: selection[0]})
    return temp


def generate_image_helper(all_images,project_name, userid):

    file_list = []
    global user_d
    global img_file_list
    global meta_file_list

    base_img_path =  BASE_DIR + '/'+ userid + '/images'
    path = BASE_DIR + '/'+ userid + '/output'
    img_path = path+'/images'
    meta_path = path+'/metadata'

    try:
        os.mkdir(img_path)
    except:
        pass
    try:
        os.mkdir(meta_path)
    except:
        pass
    
    # get images
    for k, v in all_images.items():
        meta = []
        directories = [i for i in v.keys()]
        imgnames = [i for i in v.values()]
        print(directories)
        print(imgnames)
        for x in range(0, len(directories)):
            att = {"trait_type": directories[x].split("-")[1],
                   "value": imgnames[x]}
            meta.append(att)

        # if only 2 images to combine - single pass
        if len(v) <= 2:
            im1 = PIL.Image.open(f'{base_img_path}/{directories[0]}/{imgnames[0]}.png').convert('RGBA')
            im2 = PIL.Image.open(f'{base_img_path}/{directories[1]}/{imgnames[1]}.png').convert('RGBA')
            com = PIL.Image.alpha_composite(im1, im2)
        # if > 2 images to combine - multi pass
        else:
            im1 = PIL.Image.open(f'{base_img_path}/{directories[0]}/{imgnames[0]}.png').convert('RGBA')
            im2 = PIL.Image.open(f'{base_img_path}/{directories[1]}/{imgnames[1]}.png').convert('RGBA')
            com = PIL.Image.alpha_composite(im1, im2)
            counter = 2
            while counter < len(v):
                im = PIL.Image.open(f'{base_img_path}/{directories[counter]}/{imgnames[counter]}.png').convert('RGBA')
                com = PIL.Image.alpha_composite(com, im)
                counter += 1
        
        #path = os.path.join(BASE_DIR, directory) 
        # save image
        rgb_im = com.convert('RGB')
        file = img_path+"/"+ str(k) + ".png"
        img_file_list.append(file)
        rgb_im.save(file)  

        # save metadata
        token = {
            "image": base_uri + str(k) + '.png',
            "tokenId": k,
            "name": project_name + ' ' + "#" + str(k),
            "attributes": meta
        }

        meta_file = meta_path+"/" + str(k) + '.json'
        meta_file_list.append(meta_file)
        with open(meta_file, 'w') as outfile:
            json.dump(token, outfile, indent=4)
    
    user_d[int(userid)]['meta_files'] = meta_file_list
    user_d[int(userid)]['img_files'] = img_file_list

    make_gif(img_path,userid)
    #subprocess.call(['chmod', '0o777', path])
    try:
        zip_dir(path,BASE_DIR + '/'+ userid + '/result')
    except:
        pass
    

def zip_dir(dir: Union[Path, str], filename: Union[Path, str]):
    """Zip the provided directory without navigating to that directory using `pathlib` module"""

    # Convert to Path object
    dir = Path(dir)

    with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for entry in dir.rglob("*"):
            zip_file.write(entry, entry.relative_to(dir))


def download(request):

    tuser=User.objects.get(username=getuser())
    request.session['user_id'] = tuser.id

    path_to_file = BASE_DIR + '/' + str(tuser.id) +  '/result'
    zip_file = open(path_to_file, 'rb')
    response = HttpResponse(zip_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'results.zip'
    return response

def make_gif(frame_folder,userid):
    opdir = BASE_DIR + '/' + userid
    frames = [PIL.Image.open(image) for image in glob.glob(f"{frame_folder}/*.PNG")]
    frame_one = frames[0]
    frame_one.save(opdir + "/output/my_awesome.gif", format="GIF", append_images=frames,
               save_all=True, duration=100, loop=0)



def getContract():
    return '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";

contract MyToken is ERC721, Ownable {
    constructor() ERC721("MyToken", "MTK") {}

    function _baseURI() internal pure override returns (string memory) {
        return _newuri;
    }

    function safeMint(address to, uint256 tokenId) public onlyOwner {
        _safeMint(to, tokenId);
    }
}  
  

'''
