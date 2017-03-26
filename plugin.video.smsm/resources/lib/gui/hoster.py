#-*- coding: utf-8 -*-
#Venom.
from resources.lib.handler.jdownloaderHandler import cJDownloaderHandler
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.player import cPlayer
from resources.lib.db import cDb
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.util import cUtil
import xbmc

class cHosterGui:

    SITE_NAME = 'cHosterGui'

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oGui, oHoster, sMediaUrl, sThumbnail, bGetRedirectUrl = False):
        
        #oInputParameterHandler = cInputParameterHandler()
        #aParams = oInputParameterHandler.getAllParameter()
        
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        #oGuiElement.setFunction('showHosterMenu')
        oGuiElement.setFunction('play')
        oGuiElement.setTitle(oHoster.getDisplayName())
        #oGuiElement.setThumbnail(sThumbnail)
        # if (oInputParameterHandler.exist('sMeta')):
            # sMeta = oInputParameterHandler.getValue('sMeta')
            # oGuiElement.setMeta(int(sMeta))
            
        oGuiElement.setFileName(oHoster.getFileName())
        oGuiElement.getInfoLabel()
        oGuiElement.setCat(4)
        #oGuiElement.setThumbnail(xbmc.getInfoLabel('ListItem.Art(thumb)'))
        if sThumbnail:
            oGuiElement.setThumbnail(sThumbnail)
            
        #oGuiElement.setMeta(1)
        oGuiElement.setIcon('host.png')
               
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        #oOutputParameterHandler.addParameter('sThumbnail', oGuiElement.getThumbnail())

        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())

        oOutputParameterHandler.addParameter('sTitle', oHoster.getDisplayName())
        oOutputParameterHandler.addParameter('sId', 'cHosterGui')
        oOutputParameterHandler.addParameter('siteUrl', sMediaUrl)
        #oOutputParameterHandler.addParameter('sFav', 'play')
        #oOutputParameterHandler.addParameter('sCat', '4')
        
        oGui.createContexMenuWatch(oGuiElement, oOutputParameterHandler)
        
        #context playlit menu
        oContext = cContextElement()
        oContext.setFile('cHosterGui')
        oContext.setSiteName(self.SITE_NAME)
        oContext.setFunction('addToPlaylist')
        oContext.setTitle(cConfig().getlanguage(30201))
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)
        
        #Download menu
        if (oHoster.isDownloadable() == True):
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadList')
            oContext.setTitle(cConfig().getlanguage(30202))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)
            
        if (oHoster.isDownloadable() == True):
            #Beta context download and view menu
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadListandview')
            oContext.setTitle('DL et Visualiser')
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)           
        
        #context FAV menu
        oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
        
        #context Library menu
        oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,'cLibrary','cLibrary','setLibrary','[COLOR teal]Ajouter a la librairie[/COLOR]')
      
        #bug
        oGui.addHost(oGuiElement, oOutputParameterHandler)
         
        #oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def plusHoster(self, oGui):               

        oInputParameterHandler = cInputParameterHandler()
        #aParams = oInputParameterHandler.getAllParameter()
        
        sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
        
        #formatage pour recheche serie
        sMovieTitle = cUtil().FormatSerie(sMovieTitle)
        #nettoyage pour la recherhce
        sMovieTitle = cUtil().CleanName(sMovieTitle)
        
        sUrl = "http://www.alluc.ee/stream/lang%3Aar+"+sMovieTitle
        oOutputParameterHandler = cOutputParameterHandler()

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir('alluc_ee', 'showMovies', 'Plus', 'search.png', oOutputParameterHandler)
        
        
    def checkHoster(self, sHosterUrl):
    
        #securitee
        if (not sHosterUrl):
            return False
            
        #Petit nettoyage
        sHosterUrl = sHosterUrl.split('|')[0]
        
        #Recuperation du host
        try:
            sHostName = sHosterUrl.split('/')[2]
        except:
            sHostName = sHosterUrl
       
            
        #L'user a active l'url resolver ?
        if cConfig().getSetting('UserUrlResolver') == 'true':
            import urlresolver
            hmf = urlresolver.HostedMediaFile(url=sHosterUrl)
            if hmf.valid_url():
                tmp = cHosterHandler().getHoster('resolver')
                RH = sHosterUrl.split('/')[2]
                RH = RH.replace('www.','')
                tmp.setRealHost( RH[:3].upper() )
                return tmp

        #Gestion classique
        if ('novamov' in sHostName):
            return cHosterHandler().getHoster('novamov')
        if ('userscloud' in sHostName):
            return cHosterHandler().getHoster('resolver')
        if ('vidhos' in sHostName):
            return cHosterHandler().getHoster('resolver')
        if ('watchvideo' in sHostName):
            return cHosterHandler().getHoster('resolver')
        if ('watchers' in sHostName):
            return cHosterHandler().getHoster('resolver')
        if ('bitvid' in sHostName):
            return cHosterHandler().getHoster('bitvid')
        if ('estream' in sHostName):
            return cHosterHandler().getHoster('estream')
        if ('divxstage' in sHostName):
            return cHosterHandler().getHoster('divxstage')
        if ('vidxden' in sHostName):
            return cHosterHandler().getHoster('vidxden')
        if ('vidbux' in sHostName):
            return cHosterHandler().getHoster('vidbux')
        if ('megavideo' in sHostName):
            return cHosterHandler().getHoster('megavideo')
        if ('videoweed' in sHostName):
            return cHosterHandler().getHoster('videoweed')
        if ('youwatch' in sHostName):
            return cHosterHandler().getHoster('youwatch')
        if ('turbovid' in sHostName):
            return cHosterHandler().getHoster('turbovid')
        if ('youtube' in sHostName):
            return cHosterHandler().getHoster('youtube')
        if ('youtu.be' in sHostName):
            return cHosterHandler().getHoster('youtube')
        if ('rutube' in sHostName):
            return cHosterHandler().getHoster('rutube')
        if ('exashare' in sHostName):
            return cHosterHandler().getHoster('exashare')
        if ('nowvideo' in sHostName):
            return cHosterHandler().getHoster('nowvideo')
        if ('vk.com' in sHostName):
            return cHosterHandler().getHoster('vk')
        if ('vkontakte' in sHostName):
            return cHosterHandler().getHoster('vk')
        if ('vkcom' in sHostName):
            return cHosterHandler().getHoster('vk')   
        if ('videomega' in sHostName):
            return cHosterHandler().getHoster('videomega')
        if ('vidto' in sHostName):
            return cHosterHandler().getHoster('vidto')
        if ('vidzi' in sHostName):
            return cHosterHandler().getHoster('vidzi')
        if ('cloudy' in sHostName):
            return cHosterHandler().getHoster('cloudy')
        if ('filetrip' in sHostName):
            return cHosterHandler().getHoster('filetrip')
        if ('uptostream' in sHostName):
            return cHosterHandler().getHoster('uptostream')
        if ('dailymotion' in sHostName):
            return cHosterHandler().getHoster('dailymotion')
        if ('dai.ly' in sHostName):
            return cHosterHandler().getHoster('dailymotion')           
        if ('azerfile' in sHostName):
            return cHosterHandler().getHoster('azerfile')
        if ('vodlocker' in sHostName):
            return cHosterHandler().getHoster('vodlocker')
        if ('mystream' in sHostName):
            return cHosterHandler().getHoster('mystream')
        if ('streamingentiercom/videophp?type=speed' in sHostName):
            return cHosterHandler().getHoster('speedvideo')
        if ('speedvideo' in sHostName):
            return cHosterHandler().getHoster('speedvideo')
        if ('speedvid' in sHostName):
            return cHosterHandler().getHoster('speedvid')
        if ('axavid' in sHostName):
            return cHosterHandler().getHoster('axavid') 
        if ('netu' in sHostName):
            return cHosterHandler().getHoster('netu')
        if ('hqq' in sHostName):
            return cHosterHandler().getHoster('netu')
        if ('waaw' in sHostName):
            return cHosterHandler().getHoster('netu')
        if ('mail.ru' in sHostName):
            return cHosterHandler().getHoster('mailru')
        if ('videoraj' in sHostName):
            return cHosterHandler().getHoster('videoraj')
        if ('videohut' in sHostName):
            return cHosterHandler().getHoster('videohut')
        if ('onevideo' in sHostName):
            return cHosterHandler().getHoster('onevideo')
        if ('googlevideo' in sHostName):
            return cHosterHandler().getHoster('googlevideo')
        if ('picasaweb' in sHostName):
            return cHosterHandler().getHoster('googlevideo')
        if ('googleusercontent' in sHostName):
            return cHosterHandler().getHoster('googlevideo')
        if ('video.tt' in sHostName):
            return cHosterHandler().getHoster('videott')
        if ('playreplay' in sHostName):
            return cHosterHandler().getHoster('playreplay')
        if ('streamin.to' in sHostName):
            return cHosterHandler().getHoster('streaminto')
        if ('vodlocker' in sHostName):
            return cHosterHandler().getHoster('vodlocker')
        if ('flashx' in sHostName):
            return cHosterHandler().getHoster('flashx')
        if ('easywatch' in sHostName):
            return cHosterHandler().getHoster('easywatch')
        if ('ok.ru' in sHostName):
            return cHosterHandler().getHoster('resolver')
        if ('odnoklassniki' in sHostName):
            return cHosterHandler().getHoster('resolver')
        if ('vimeo.com' in sHostName):
            return cHosterHandler().getHoster('vimeo')
        if ('openload' in sHostName):
            return cHosterHandler().getHoster('openload')
        if ('oload.co' in sHostName):
            return cHosterHandler().getHoster('openload')
        if ('thevideo.me' in sHostName):
            return cHosterHandler().getHoster('thevideo_me')    
        if ('vid.me' in sHostName):
            return cHosterHandler().getHoster('vidme')
        if ('zstream' in sHostName):
            return cHosterHandler().getHoster('zstream')
        if ('watching' in sHostName):
            return cHosterHandler().getHoster('watching')
        if ('letwatch' in sHostName):
            return cHosterHandler().getHoster('letwatch')
        if ('easyvid' in sHostName):
            return cHosterHandler().getHoster('easyvid')
        if ('allvid' in sHostName):
            return cHosterHandler().getHoster('allvid')
        if ('www.amazon' in sHostName):
            return cHosterHandler().getHoster('amazon')
        if ('filepup' in sHostName):
            return cHosterHandler().getHoster('filepup')
        if ('v-vids' in sHostName):
            return cHosterHandler().getHoster('v_vids')
        if ('vid.ag' in sHostName):
            return cHosterHandler().getHoster('vid_ag')
        if ('wat.tv' in sHostName):
            return cHosterHandler().getHoster('wat_tv')
        if ('thevid' in sHostName):
            return cHosterHandler().getHoster('thevid')
        if ('nosvideo' in sHostName):
            return cHosterHandler().getHoster('nosvideo')
        if ('player.vimple.ru' in sHostName):
            return cHosterHandler().getHoster('vimple')
        if ('allmyvideos.net' in sHostName):
            return cHosterHandler().getHoster('allmyvideos')
        if ('idowatch' in sHostName):
            return cHosterHandler().getHoster('idowatch')
        if ('wstream.' in sHostName):
            return cHosterHandler().getHoster('wstream')
        if ('veevr.' in sHostName):
            return cHosterHandler().getHoster('veevr')
        if ('watchvideo.' in sHostName):
             return cHosterHandler().getHoster('watchvideo')
        if ('drive.google.com' in sHostName):
            return cHosterHandler().getHoster('googledrive')
        if ('docs.google.com' in sHostName):
            return cHosterHandler().getHoster('googledrive')
        if ('vidwatch' in sHostName):
            return cHosterHandler().getHoster('vidwatch')
        if ('up2stream' in sHostName):
            return cHosterHandler().getHoster('up2stream')

        #Lien telechargeable a convertir en stream
        if ('1fichier' in sHostName):
            return cHosterHandler().getHoster('onefichier')
        if ('uptobox' in sHostName):
            return cHosterHandler().getHoster('uptobox')
        if ('uplea.com' in sHostName):
            return cHosterHandler().getHoster('uplea')            
        if ('uploaded' in sHostName or 'ul.to' in sHostName):
            return cHosterHandler().getHoster('uploaded')            
        if ('mp4' in sHostName):
            return cHosterHandler().getHoster('lien_direct')            
        if ('panet' in sHostName):
            return cHosterHandler().getHoster('lien_direct')            
        if ('moshahda' in sHostName):
            return cHosterHandler().getHoster('lien_direct')
            
        #Si aucun hebergeur connu on teste les liens directs
        if (sHosterUrl[-4:] in '.mp4.avi.flv.m3u8'):
            return cHosterHandler().getHoster('lien_direct')
            
        #module resolver HS
        #try:
        #    import urlresolver
        #    host = urlresolver.HostedMediaFile(sHosterUrl)
        #    if host:
        #        return cHosterHandler().getHoster('resolver')
        #except:
        #    pass

        return False
        
        # step 2
        
        
    # def showHosterMenu(self):
        # oGui = cGui()
        # oInputParameterHandler = cInputParameterHandler()

        # sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        # sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        # bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        # sFileName = oInputParameterHandler.getValue('sFileName')

        # oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        # oHoster.setFileName(sFileName)

        # # play
        # self.__showPlayMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl)

        # # playlist
        # self.__showPlaylistMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl)

        # # download
        # if (oHoster.isDownloadable() == True):
            # self.__showDownloadMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl)        

        # # JD
        # if (oHoster.isJDownloaderable() == True):
            # self.__showJDMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl)    

        # oGui.setEndOfDirectory()

    # def __showPlayMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl):
        # oGuiElement = cGuiElement()
        # oGuiElement.setSiteName(self.SITE_NAME)
        # oGuiElement.setFunction('play')
        # oGuiElement.setTitle('play')
        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        # oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        # oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        # oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        # oGui.addFolder(oGuiElement, oOutputParameterHandler)

    # def __showDownloadMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl):
        # oGuiElement = cGuiElement()
        # oGuiElement.setSiteName(self.SITE_NAME)
        # oGuiElement.setFunction('download')
        # oGuiElement.setTitle('download ueber XBMC')
        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        # oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        # oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        # oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        # oGui.addFolder(oGuiElement, oOutputParameterHandler)

    # def __showJDMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl):
        # oGuiElement = cGuiElement()
        # oGuiElement.setSiteName(self.SITE_NAME)        
        # oGuiElement.setTitle('an JDownloader senden')
        # oGuiElement.setFunction('sendToJDownbloader')
        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        # oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        # oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        # oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        # oGui.addFolder(oGuiElement, oOutputParameterHandler)

    # def __showPlaylistMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl):
        # oGuiElement = cGuiElement()
        # oGuiElement.setSiteName(self.SITE_NAME)
        # oGuiElement.setFunction('addToPlaylist')
        # oGuiElement.setTitle('add to playlist')
        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        # oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        # oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        # oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        # oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def play(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')
        #sThumbnail = oInputParameterHandler.getValue('sThumbnail')

        if (bGetRedirectUrl == 'True'):            
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        cConfig().log("Hoster - play " + sMediaUrl)

        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        sHosterName = oHoster.getDisplayName()
        cConfig().showInfo(sHosterName, 'Resolve')
        
        #oHoster.setUrl(sMediaUrl)
        #aLink = oHoster.getMediaLink()
        
        try:
        
            oHoster.setUrl(sMediaUrl)
            aLink = oHoster.getMediaLink()

            if (aLink[0] == True):
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(self.SITE_NAME)
                oGuiElement.setMediaUrl(aLink[1])
                oGuiElement.setTitle(oHoster.getFileName())
                oGuiElement.getInfoLabel()
                
                oPlayer = cPlayer()
                oPlayer.run(oGuiElement, oHoster.getFileName(), aLink[1])
                
                # oGuiElement = cGuiElement()
                # oGuiElement.setSiteName(self.SITE_NAME)
                # oGuiElement.setMediaUrl(aLink[1])
                # oGuiElement.setTitle(oHoster.getFileName())
                # oGuiElement.getInfoLabel()
                
                # oPlayer = cPlayer()
                # oPlayer.clearPlayList()
                # oPlayer.addItemToPlaylist(oGuiElement)
                # oPlayer.startPlayer()
                return
            else:
                #cConfig().showInfo(sHosterName, 'file not found')
                cConfig().error("file not found ")
                return

        except:
            #cConfig().showInfo(sHosterName, 'file not found')
            cConfig().error("file not found ")
            return

        oGui.setEndOfDirectory()

    def addToPlaylist(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')
        

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        cConfig().log("Hoster - play " + sMediaUrl)
        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        #try:

        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()

        if (aLink[0] == True):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])
            oGuiElement.setTitle(oHoster.getFileName())

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            oGui.showInfo('Playlist', str(oHoster.getFileName()), 5);
            return

        #except:
        # cConfig().log("could not load plugin " + sHosterFileName)

        oGui.setEndOfDirectory()
        

    # def download(self):
        # oGui = cGui()
        # oInputParameterHandler = cInputParameterHandler()

        # sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        # sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        # bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        # sFileName = oInputParameterHandler.getValue('sFileName')

        # if (bGetRedirectUrl == 'True'):
            # sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        # cConfig().log("Telechargement " + sMediaUrl)

        # oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        # oHoster.setFileName(sFileName)

        # #try:
        # oHoster.setUrl(sMediaUrl)
        # aLink = oHoster.getMediaLink()
        # if (aLink[0] == True):
            # oDownload = cDownload()
            # oDownload.download(aLink[1], oHoster.getFileName())
            # return

        # #except:
        # # cConfig().log("Telechargement " + sHosterFileName)

        # oGui.setEndOfDirectory()

    def sendToJDownbloader(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)
        oHoster.setUrl(sMediaUrl)
        sMediaUrl = oHoster.getUrl()

        cConfig().log("Telechargement jdownloader " + sMediaUrl)

        cJDownloaderHandler().sendToJDownloader(sMediaUrl)


    def __getRedirectUrl(self, sUrl):
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()

        

       
