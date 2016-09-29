-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: jandan
-- ------------------------------------------------------
-- Server version	5.1.73

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `jandan`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `jandan` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `jandan`;

--
-- Table structure for table `configs`
--

DROP TABLE IF EXISTS `configs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configs` (
  `config` varchar(20) CHARACTER SET utf8 NOT NULL,
  `info` varchar(2000) CHARACTER SET utf8 NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configs`
--

LOCK TABLES `configs` WRITE;
/*!40000 ALTER TABLE `configs` DISABLE KEYS */;
INSERT INTO `configs` VALUES ('page_num','2147'),('agent','\'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0\',\'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36\',\'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393\',\'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729\'');
/*!40000 ALTER TABLE `configs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ooxx`
--

DROP TABLE IF EXISTS `ooxx`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ooxx` (
  `url` varchar(255) NOT NULL,
  `oo` varchar(20) NOT NULL,
  `xx` varchar(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ooxx`
--

LOCK TABLES `ooxx` WRITE;
/*!40000 ALTER TABLE `ooxx` DISABLE KEYS */;
INSERT INTO `ooxx` VALUES ('http://ww2.sinaimg.cn/large/9f8c5e89gw1f89sh4h0ngj20h61hcq6z.jpg','175','21'),('http://ww2.sinaimg.cn/large/006fVPCvjw1f7hi02h8zsj318g18gh2l.jpg','183','11'),('http://ww2.sinaimg.cn/large/a00dfa2agw1f7hfwtlcywg208g07k1ky.gif','218','24'),('http://ww3.sinaimg.cn/large/a00dfa2agw1f7hb9n7oboj20zk1hcgzh.jpg','210','11'),('http://ww3.sinaimg.cn/large/6cca1403jw1f7h7d1tzsjj20h20grwf2.jpg','175','11'),('http://ww4.sinaimg.cn/large/005vbOHfgw1f7gkkxe33kj30zk1hc449.jpg','167','14'),('http://ww1.sinaimg.cn/large/005vbOHfgw1f7gkkt8euwj30gn0nn0uy.jpg','294','13'),('http://ww2.sinaimg.cn/large/005vbOHfgw1f7gkl0td32j30jg0scgqu.jpg','162','21'),('http://ww3.sinaimg.cn/large/6fcc980cgw1f7iuz1v5roj20af0fxaax.jpg','388','19'),('http://ww3.sinaimg.cn/large/3e3666efjw1f7fee5xyqng208r06mx6q.gif','268','8'),('http://ww4.sinaimg.cn/large/b2b1bff9jw1f7heyzh73tg20e409o1kz.gif','194','25'),('http://ww4.sinaimg.cn/large/7c0f6495jw1f7hyy8t9mjg20b408c7wh.gif','408','27'),('http://ww2.sinaimg.cn/large/6469180ajw1f7hirxkmomj20u017jnc5.jpg','187','26'),('http://ww2.sinaimg.cn/large/005vbOHfgw1f7hpr0qv2ej30cc0limzx.jpg','305','28'),('http://ww3.sinaimg.cn/large/005vbOHfgw1f7hpqu561rj30ff0rxwj3.jpg','252','22'),('http://ww3.sinaimg.cn/large/005vbOHfgw1f7k1c2wqmej30d70ls77z.jpg','296','24'),('http://ww2.sinaimg.cn/large/006fVPCvjw1f7jsjuqn1ej30mr0sgq6w.jpg','787','22'),('http://ww4.sinaimg.cn/large/006fVPCvjw1f7jsg86bvcj311x1kw1ae.jpg','152','9'),('http://ww3.sinaimg.cn/large/44e703b9gw1f7jnqupxibj20cu0fqq3k.jpg','351','30'),('http://ww1.sinaimg.cn/large/a00dfa2agw1f7hjtmh2mwg209m09qe83.gif','365','21'),('http://ww4.sinaimg.cn/large/006fVPCvjw1f7m5kibadmj311x1kwwi1.jpg','224','13'),('http://ww2.sinaimg.cn/large/006fVPCvjw1f7m5jlpbw5j30vj18gq8v.jpg','211','17'),('http://ww3.sinaimg.cn/large/a00dfa2agw1f7le6rhyyej20mj10n7bj.jpg','262','30'),('http://ww4.sinaimg.cn/large/005vbOHfgw1f7l7bfetcoj30du0kuwfc.jpg','371','12'),('http://ww4.sinaimg.cn/large/005vbOHfgw1f7l77ofst4j30b50goace.jpg','333','16'),('http://ww1.sinaimg.cn/large/3e3666efjw1f7k2h9zxe0g20dw07rnph.gif','211','24'),('http://ww3.sinaimg.cn/large/006xvkvkgw1f7mo24gxq9g30c607enpd.gif','200','30'),('http://ww1.sinaimg.cn/large/6cca1403jw1f7knsfdhoxj20f90haq3j.jpg','309','19'),('http://ww4.sinaimg.cn/large/006977Htjw1f7m4t838oxg30c607enpd.gif','179','20'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7m8x04580j20lc0sgmzy.jpg','245','25'),('http://ww2.sinaimg.cn/large/9ff9594fgw1f7o5jl42r7j20eo0l3wkn.jpg','255','24'),('http://ww1.sinaimg.cn/large/7c0f6495jw1f7nqs7y4vyj20te186k6x.jpg','755','30'),('http://ww3.sinaimg.cn/large/7c0f6495jw1f7nqh0q4p4j20p00xcn1z.jpg','321','24'),('http://ww1.sinaimg.cn/large/005vbOHfgw1f7nlbg4o2rj30u00r4dhv.jpg','262','20'),('http://ww2.sinaimg.cn/large/3e3666efjw1f7n23bcpajg20cs08iqi8.gif','465','28'),('http://ww3.sinaimg.cn/large/005vbOHfgw1f7puouhibnj30nc0zxdkm.jpg','224','20'),('http://ww4.sinaimg.cn/large/005vbOHfgw1f7pup4mveij30qf15o47x.jpg','214','25'),('http://ww4.sinaimg.cn/large/a15b4afegw1f7pt6u961zj20zk0npq86.jpg','192','30'),('http://ww4.sinaimg.cn/large/53ae0b70jw1f7pin3q18cg20b4069qin.gif','268','24'),('http://ww3.sinaimg.cn/large/6469180ajw1f7k3kahnv0j20jg0t6jvp.jpg','159','22'),('http://ww3.sinaimg.cn/large/a00dfa2agw1f7phqqkmvvj20sd18gtj2.jpg','197','11'),('http://ww2.sinaimg.cn/large/a00dfa2agw1f7pcg42vthj20m80gognj.jpg','523','26'),('http://ww3.sinaimg.cn/large/005vbOHfgw1f7ot8qvf3kj30jg0t6adu.jpg','158','20'),('http://ww3.sinaimg.cn/large/005vbOHfgw1f7ot5rz8m3j30ia0riwj9.jpg','165','14'),('http://ww1.sinaimg.cn/large/6b479262gw1f7opnp5u82j21jk27ih9e.jpg','154','26'),('http://ww4.sinaimg.cn/large/66b3de17gw1f79s64ifl2j20go0pajt2.jpg','185','14'),('http://ww3.sinaimg.cn/large/66b3de17gw1f7q03ndkwaj20fv0ml0u8.jpg','411','20'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7q03mmsy4j20go0m83zm.jpg','301','9'),('http://ww4.sinaimg.cn/large/66b3de17gw1f7q03m9pl4j20go0cyt99.jpg','219','20'),('http://ww4.sinaimg.cn/large/66b3de17gw1f7q03kpe4xj20go0kr76a.jpg','238','14'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7q03jxgwfj20go0ci74q.jpg','170','19'),('http://ww2.sinaimg.cn/large/66b3de17gw1f7q03hc3wvj20go0kqju3.jpg','159','17'),('http://ww1.sinaimg.cn/large/005vbOHfgw1f7s5grp258j30jg0t9tde.jpg','279','14'),('http://ww3.sinaimg.cn/large/3e3666efjw1f5gjkizhn3g208p06k1l1.gif','380','12'),('http://ww4.sinaimg.cn/large/3e3666efjw1f5tb42qf3jg208p06ke84.gif','269','12'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7q03oz0ppj20go0mzn0m.jpg','216','17'),('http://ww1.sinaimg.cn/large/0069lnCQjw1f7ro1aqxouj30zk1hcgsl.jpg','214','22'),('http://ww4.sinaimg.cn/large/0069lnCQjw1f7ro0ilequj30hq0qoq4q.jpg','181','18'),('http://ww4.sinaimg.cn/large/005vbOHfgw1f7r0avfpljj31kw1ivwpo.jpg','335','15'),('http://ww2.sinaimg.cn/large/005vbOHfgw1f7r0aoruxnj30go0p0q6c.jpg','216','16'),('http://ww4.sinaimg.cn/large/a82b014bjw1exuum36eaqg20ge0a0npi.gif','214','20'),('http://ww2.sinaimg.cn/large/a82b014bjw1exkpdup88ej20dw0kuwk4.jpg','199','24'),('http://ww4.sinaimg.cn/large/a82b014bjw1f7tadv2kxyg20gi0841lf.gif','226','18'),('http://ww1.sinaimg.cn/large/6822fff7gw1f7sz1ykbd9j20m80wg0vh.jpg','167','26'),('http://ww2.sinaimg.cn/large/7c0f6495jw1f7sc8ddgbyj20qe0qotbz.jpg','330','22'),('http://ww2.sinaimg.cn/large/66b3de17gw1f7tj7ehgqrj20rp0rsadv.jpg','186','21'),('http://ww2.sinaimg.cn/large/66b3de17gw1f7tj7d33g5j20qo0zkdks.jpg','191','19'),('http://ww3.sinaimg.cn/large/66b3de17gw1f7tj8deoioj20go0p0ac0.jpg','394','23'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7tj8dqlg4j20hs0qpdje.jpg','207','19'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7tj77rx9vj20dv0kujuf.jpg','179','25'),('http://ww4.sinaimg.cn/large/66b3de17gw1f7tj6l2sopj20bx0hsgni.jpg','432','28'),('http://ww1.sinaimg.cn/large/7c0f6495jw1f7tj0afa34j20k00qotac.jpg','458','13'),('http://ww4.sinaimg.cn/large/66b3de17gw1f7uje1zl29j20pk0vxjub.jpg','162','12'),('http://ww3.sinaimg.cn/large/b2b1bff9jw1f7sfknw6fgj20et0l9mz4.jpg','362','9'),('http://ww2.sinaimg.cn/large/66b3de17gw1f7tj7qhxhxj20zk1hck47.jpg','161','22'),('http://ww4.sinaimg.cn/large/0064BOeZjw1f7s458b6cyj30lc0sgwgu.jpg','152','22'),('http://ww3.sinaimg.cn/large/66b3de17gw1f7tj8aiitzj20dw0kugnf.jpg','206','16'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7tj8bb64bj20y41hcjxv.jpg','196','15'),('http://ww3.sinaimg.cn/large/66b3de17gw1f7tj84mk3dj20lc0sgjti.jpg','246','30'),('http://ww4.sinaimg.cn/large/64bd7fffgw1f7up1qeewuj20xc0xpdlk.jpg','261','28'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7ujdt4n71j20go0tntam.jpg','170','17'),('http://ww3.sinaimg.cn/large/a00dfa2agw1f7vsdzejnsj20hs0hs0uc.jpg','203','26'),('http://ww3.sinaimg.cn/large/ba05abb3gw1ehytz9e1j0g209q09qk7e.gif','223','12'),('http://ww3.sinaimg.cn/large/d52454acgw1f7vjljrc6lj20dw0j9t9d.jpg','225','26'),('http://ww2.sinaimg.cn/large/ab758504gw1f6mdf25macj21hc13rqfq.jpg','177','28'),('http://ww1.sinaimg.cn/large/6e6bf3aegw1f74s7j49adj21e00xd4d1.jpg','155','11'),('http://ww4.sinaimg.cn/large/ed46c01egw1f7rsg2iq7jj20qo0qon42.jpg','167','10'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7tj887pqbj20ij0rszoa.jpg','221','21'),('http://ww4.sinaimg.cn/large/66b3de17gw1f7tj89beaej20g40o5adz.jpg','165','17'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7tj89cqmej20qo0zkadj.jpg','309','21'),('http://ww4.sinaimg.cn/large/66b3de17gw1f7ujdvz8o5j20go0m70tw.jpg','159','10'),('http://ww2.sinaimg.cn/large/b7d0ddabjw1f7vtj349o9j20ia0wijvl.jpg','595','25'),('http://ww3.sinaimg.cn/large/b2b1bff9jw1f7ao7mufytj20f00k0q3f.jpg','440','29'),('http://ww4.sinaimg.cn/large/721170b1jw1f7xosxjsooj21ao1y0e1s.jpg','151','7'),('http://ww3.sinaimg.cn/large/721170b1jw1f7xocf9cn7j20dw0k9acs.jpg','184','22'),('http://ww3.sinaimg.cn/large/b2b1bff9jw1f7vimz1kw1j20qo0zkwh7.jpg','315','7'),('http://ww2.sinaimg.cn/large/005vbOHfgw1f7xf1hrq8cj30go0p0423.jpg','220','12'),('http://ww4.sinaimg.cn/large/005vbOHfgw1f7xf2ne95ej30g70qkdkx.jpg','308','17'),('http://ww3.sinaimg.cn/large/6469180ajw1f7wj5ze4jwj20eg0hztaj.jpg','155','30'),('http://ww1.sinaimg.cn/large/b7d0ddabjw1f7wpjoakqng208c05ix6p.gif','244','12'),('http://ww2.sinaimg.cn/large/66b3de17gw1f7wv8k478vj20zk1cr4ef.jpg','178','9'),('http://ww2.sinaimg.cn/large/a00dfa2agw1f7y11ew965j20ik0oqq4j.jpg','182','10'),('http://ww3.sinaimg.cn/large/66b3de17gw1f7wv8m1v7jj20tn18g0z9.jpg','172','7'),('http://ww3.sinaimg.cn/large/5809ec90gw1f7xim9i9bfj20nm0zkgp5.jpg','198','12'),('http://ww2.sinaimg.cn/large/66b3de17gw1f7wv8s4n8kj20zk0np412.jpg','201','13'),('http://ww2.sinaimg.cn/large/66b3de17gw1f7wv8x9ie7j20ma0xcgty.jpg','282','12'),('http://ww4.sinaimg.cn/large/aa594a48gw1f7yupcjxa3j20m80et0ts.jpg','859','30'),('http://ww2.sinaimg.cn/large/66b3de17gw1f7wv8fijh4j20ug19ph0s.jpg','268','26'),('http://ww4.sinaimg.cn/large/6e158bb7jw1f7zxh6hgc9g206y05kx5g.gif','193','9'),('http://ww2.sinaimg.cn/large/721170b1jw1f7zfmv445aj20hs0mwdkw.jpg','184','12'),('http://ww3.sinaimg.cn/large/721170b1jw1f7zfmqmeg2j20zk1hc7l4.jpg','332','23'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7wvdccamyj20du0ku76k.jpg','234','18'),('http://ww3.sinaimg.cn/large/66b3de17gw1f7wvd2o8h8j20rs15o0zx.jpg','173','6'),('http://ww2.sinaimg.cn/large/66b3de17gw1f7wv80krakj20cl0gsq3y.jpg','250','8'),('http://ww3.sinaimg.cn/large/005vbOHfgw1f81jjn9o3qj30hs0qo43b.jpg','237','14'),('http://ww2.sinaimg.cn/large/005vbOHfgw1f81jjr6oytj30ia0sbtal.jpg','233','24'),('http://ww3.sinaimg.cn/large/721170b1jw1f81efm5nblj20rs0ygwlw.jpg','150','7'),('http://ww2.sinaimg.cn/large/721170b1jw1f81eeemyrzj20b4069q3i.jpg','316','18'),('http://ww3.sinaimg.cn/large/721170b1jw1f81dws63v0j20hs0rwn27.jpg','223','25'),('http://ww2.sinaimg.cn/large/721170b1jw1f81dwu2l9uj20h80mwq3j.jpg','239','22'),('http://ww3.sinaimg.cn/large/66b3de17gw1f7wvdlhx9pj20m80xcgph.jpg','187','16'),('http://ww4.sinaimg.cn/large/721170b1jw1f81sskvlt7j20dw09amz6.jpg','151','20'),('http://ww4.sinaimg.cn/large/721170b1jw1f81socrmyhj20ia0wijvl.jpg','240','14'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7wvdot7jwj20v516x7a3.jpg','153','13'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7wvdmphu1j20ca0ifq5i.jpg','201','19'),('http://ww1.sinaimg.cn/large/005vbOHfgw1f81jqn050wg30hp09j1l3.gif','285','25'),('http://ww2.sinaimg.cn/large/005vbOHfgw1f82pev471nj30go0j3go8.jpg','255','12'),('http://ww2.sinaimg.cn/large/73f627b9gw1f82gruyq6uj20np0zk10s.jpg','172','18'),('http://ww2.sinaimg.cn/large/bd698b0fjw1f72bmy7s0sj20q70ihwfp.jpg','300','24'),('http://ww2.sinaimg.cn/large/7c0f6495jw1f83vgahv52j20hs0mjn2s.jpg','278','28'),('http://ww2.sinaimg.cn/large/7c0f6495jw1f83vgdg6exg20b4065x6p.gif','193','10'),('http://ww2.sinaimg.cn/large/02792b17gw1f83mlss1pzg20dc0hqasu.gif','150','22'),('http://ww3.sinaimg.cn/large/66b3de17gw1f826dg4s9yj20go0got9t.jpg','173','14'),('http://ww3.sinaimg.cn/large/66b3de17gw1f7wve4jt60j20rs15otew.jpg','166','20'),('http://ww4.sinaimg.cn/large/66b3de17gw1f7wve3g6hxj20qm0zktjs.jpg','208','28'),('http://ww1.sinaimg.cn/large/66b3de17gw1f826dlven0j20pk0pk415.jpg','216','12'),('http://ww4.sinaimg.cn/large/66b3de17gw1f7wv97xdo2j20nm0zkwja.jpg','150','8'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7wv9jjtwwj20m80u6tb3.jpg','166','15'),('http://ww4.sinaimg.cn/large/005vbOHfgw1f851jo68zbj31jk2bc19k.jpg','168','28'),('http://ww1.sinaimg.cn/large/4bf31e43jw1f850u0n248g209l0an7wr.gif','302','20'),('http://ww1.sinaimg.cn/large/4bf31e43jw1f850tl9dtpg20do0624qt.gif','234','12'),('http://ww3.sinaimg.cn/large/005vbOHfgw1f84udu4bsaj30ia0iaq48.jpg','283','21'),('http://ww3.sinaimg.cn/large/695105e0gw1f84u1zi87cg20ad06o1l0.gif','310','19'),('http://ww2.sinaimg.cn/large/6cca1403jw1f7wmp87ua2j20e90hoabu.jpg','258','14'),('http://ww2.sinaimg.cn/large/005vbOHfgw1f85zz4rtq0j30s60gyjtg.jpg','174','20'),('http://ww1.sinaimg.cn/large/005vbOHfgw1f85zyx3uonj30jg0t678l.jpg','152','21'),('http://ww3.sinaimg.cn/large/005vbOHfgw1f85zytvf6zj30go0j3go8.jpg','243','14'),('http://ww2.sinaimg.cn/large/721170b1jw1f85z6y85lvj20dw08o3zo.jpg','182','9'),('http://ww3.sinaimg.cn/large/721170b1jw1f85z6whqj0j20dw09aaa5.jpg','298','21'),('http://ww1.sinaimg.cn/large/9f8c5e89gw1f824vu7vjjj20no0ugq7b.jpg','207','18'),('http://ww1.sinaimg.cn/large/005vbOHfgw1f8748u21hpj30v318gq78.jpg','176','22'),('http://ww2.sinaimg.cn/large/005vbOHfgw1f8749epx7qj30hs0vk76x.jpg','150','18'),('http://ww1.sinaimg.cn/large/005vbOHfgw1f874b03ie0j30hz0uw0wr.jpg','383','22'),('http://ww1.sinaimg.cn/large/8a665039gw1f86m4h4xvjj20u01hc17h.jpg','266','15'),('http://ww3.sinaimg.cn/large/66b3de17gw1f7wv9v5331j20oz11hdry.jpg','214','19'),('http://ww4.sinaimg.cn/large/66b3de17gw1f7wv9pmrbuj20es0m8abo.jpg','161','10'),('http://ww3.sinaimg.cn/large/005vbOHfgw1f89bzz1w2vj31kw11x0z7.jpg','212','16'),('http://ww3.sinaimg.cn/large/3e3666efjw1f8966fi9ygg208r06mu10.gif','151','25'),('http://ww1.sinaimg.cn/large/005vbOHfgw1f88awhbscqj30k00qodhc.jpg','183','27'),('http://ww3.sinaimg.cn/large/005vbOHfgw1f88awlgrpnj30c80ijq45.jpg','261','10'),('http://ww2.sinaimg.cn/large/005vbOHfgw1f88awp6vlzj30fa0hjdgt.jpg','238','22'),('http://ww1.sinaimg.cn/large/66b3de17gw1f7wva5yw4aj20m80xcn52.jpg','190','18'),('http://ww3.sinaimg.cn/large/66b3de17gw1f7wva555hjj20np0zkdja.jpg','156','18');
/*!40000 ALTER TABLE `ooxx` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-09-29 11:19:13
