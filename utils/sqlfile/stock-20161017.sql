-- MySQL Script generated by MySQL Workbench
-- Thu May  5 11:24:44 2016
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema stock
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `stock` ;

-- -----------------------------------------------------
-- Schema stock
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `stock` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `stock` ;

DROP TABLE IF EXISTS `asst_liab_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asst_liab_table` (
  `year` char(4) NOT NULL,
  `period` varchar(8) NOT NULL,
  `stock_cd` varchar(6) NOT NULL,
  `data_sour` varchar(20) NOT NULL,
  `curr_fund` decimal(24,2) DEFAULT NULL,
  `notes_recev` decimal(24,2) DEFAULT NULL,
  `txn_fin_ast` decimal(24,2) DEFAULT NULL,
  `reces` decimal(24,2) DEFAULT NULL,
  `prepay` decimal(24,2) DEFAULT NULL,
  `oth_recev` decimal(24,2) DEFAULT NULL,
  `recev_afflt_account` decimal(24,2) DEFAULT NULL,
  `recev_intr` decimal(24,2) DEFAULT NULL,
  `recev_dividn` decimal(24,2) DEFAULT NULL,
  `inventy` decimal(24,2) DEFAULT NULL,
  `consum_bio_ast` decimal(24,2) DEFAULT NULL,
  `oyear_not_current_ast` decimal(24,2) DEFAULT NULL,
  `other_current_ast` decimal(24,2) DEFAULT NULL,
  `current_ast_sum` decimal(24,2) DEFAULT NULL,
  `saleable_fin_ast` decimal(24,2) DEFAULT NULL,
  `hold_investm_due` decimal(24,2) DEFAULT NULL,
  `lterm_reces` decimal(24,2) DEFAULT NULL,
  `lterm_equity_investm` decimal(24,2) DEFAULT NULL,
  `real_estate_investm` decimal(24,2) DEFAULT NULL,
  `fixed_ast` decimal(24,2) DEFAULT NULL,
  `under_constr_proj` decimal(24,2) DEFAULT NULL,
  `proj_goods` decimal(24,2) DEFAULT NULL,
  `fixed_ast_clean` decimal(24,2) DEFAULT NULL,
  `prod_bio_ast` decimal(24,2) DEFAULT NULL,
  `oil_ast` decimal(24,2) DEFAULT NULL,
  `intang_ast` decimal(24,2) DEFAULT NULL,
  `develop_costs` decimal(24,2) DEFAULT NULL,
  `goodwill` decimal(24,2) DEFAULT NULL,
  `deferred_ast` decimal(24,2) DEFAULT NULL,
  `deferred_tax_ast` decimal(24,2) DEFAULT NULL,
  `oth_non_current_ast` decimal(24,2) DEFAULT NULL,
  `non_current_ast_sum` decimal(24,2) DEFAULT NULL,
  `ast_sum` decimal(24,2) DEFAULT NULL,
  `sterm_liab` decimal(24,2) DEFAULT NULL,
  `txn_fin_liab` decimal(24,2) DEFAULT NULL,
  `notes_payable` decimal(24,2) DEFAULT NULL,
  `accounts_payable` decimal(24,2) DEFAULT NULL,
  `adv_account` decimal(24,2) DEFAULT NULL,
  `payroll_payable` decimal(24,2) DEFAULT NULL,
  `tax_payable` decimal(24,2) DEFAULT NULL,
  `intr_payable` decimal(24,2) DEFAULT NULL,
  `dividn_payable` decimal(24,2) DEFAULT NULL,
  `oth_payable` decimal(24,2) DEFAULT NULL,
  `due_related_corp` decimal(24,2) DEFAULT NULL,
  `oyear_not_current_liab` decimal(24,2) DEFAULT NULL,
  `oth_current_liab` decimal(24,2) DEFAULT NULL,
  `current_liab_sum` decimal(24,2) DEFAULT NULL,
  `ltrem_loan` decimal(24,2) DEFAULT NULL,
  `bonds_payable` decimal(24,2) DEFAULT NULL,
  `term_payable` decimal(24,2) DEFAULT NULL,
  `estim_liab` decimal(24,2) DEFAULT NULL,
  `deferr_inc_tax_liab` decimal(24,2) DEFAULT NULL,
  `oth_not_current_liab` decimal(24,2) DEFAULT NULL,
  `not_current_liab_sum` decimal(24,2) DEFAULT NULL,
  `liab_sum` decimal(24,2) DEFAULT NULL,
  `real_reces_cap` decimal(24,2) DEFAULT NULL,
  `cap_reserve` decimal(24,2) DEFAULT NULL,
  `earned_surplus` decimal(24,2) DEFAULT NULL,
  `treas_stock` decimal(24,2) DEFAULT NULL,
  `undistr_profit` decimal(24,2) DEFAULT NULL,
  `minority_equity` decimal(24,2) DEFAULT NULL,
  `fcurr_trans_spreads` decimal(24,2) DEFAULT NULL,
  `abnorm_run_proj_inc_adjust` decimal(24,2) DEFAULT NULL,
  `owner_intr_sum` decimal(24,2) DEFAULT NULL,
  `liab_owner_sum` decimal(24,2) DEFAULT NULL,
  `modifytime` varchar(19) DEFAULT NULL,
  `spec_payable` decimal(24,2) DEFAULT NULL,
  PRIMARY KEY (`year`,`period`,`stock_cd`,`data_sour`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cash_flow_table`
--

DROP TABLE IF EXISTS `cash_flow_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cash_flow_table` (
  `year` char(4) NOT NULL,
  `period` varchar(8) NOT NULL,
  `stock_cd` varchar(6) NOT NULL,
  `data_sour` varchar(20) NOT NULL,
  `cash_recev_sell_goods` decimal(24,2) DEFAULT NULL,
  `refund_taxes` decimal(24,2) DEFAULT NULL,
  `cash_recev_oth_run_biz` decimal(24,2) DEFAULT NULL,
  `operat_activ_cash_inflows` decimal(24,2) DEFAULT NULL,
  `cash_paid_buy_goods` decimal(24,2) DEFAULT NULL,
  `tax_paym` decimal(24,2) DEFAULT NULL,
  `cash_paid_staff` decimal(24,2) DEFAULT NULL,
  `cash_paid_oth_run_biz` decimal(24,2) DEFAULT NULL,
  `operat_activ_cash_outflow` decimal(24,2) DEFAULT NULL,
  `operat_activ_cash_flow_Net` decimal(24,2) DEFAULT NULL,
  `cash_recev_invests` decimal(24,2) DEFAULT NULL,
  `cash_recev_invest_intr` decimal(24,2) DEFAULT NULL,
  `net_cash_recev_disp_fix_ast` decimal(24,2) DEFAULT NULL,
  `net_cash_recev_oth_biz` decimal(24,2) DEFAULT NULL,
  `recev_oth_invest_activ_cash` decimal(24,2) DEFAULT NULL,
  `cash_inflow_invest_activ` decimal(24,2) DEFAULT NULL,
  `cash_paid_constr_fixed_ast` decimal(24,2) DEFAULT NULL,
  `inv_payment` decimal(24,2) DEFAULT NULL,
  `net_cash_acqu_oth_biz_units` decimal(24,2) DEFAULT NULL,
  `pay_oth_invest_activ_cash` decimal(24,2) DEFAULT NULL,
  `cash_outflow_invest_activ` decimal(24,2) DEFAULT NULL,
  `net_cashflow_make_invest_activ` decimal(24,2) DEFAULT NULL,
  `cash_recev_invest` decimal(24,2) DEFAULT NULL,
  `cash_recev_debts` decimal(24,2) DEFAULT NULL,
  `oth_fin_activ_recv_cash` decimal(24,2) DEFAULT NULL,
  `fina_activ_cash_inflow` decimal(24,2) DEFAULT NULL,
  `debt_payment` decimal(24,2) DEFAULT NULL,
  `pay_intr_cash` decimal(24,2) DEFAULT NULL,
  `cash_payment_rela_fina_activ` decimal(24,2) DEFAULT NULL,
  `cash_outflow_fina_activ` decimal(24,2) DEFAULT NULL,
  `ncash_flow_make_fina_activ` decimal(24,2) DEFAULT NULL,
  `modifytime` varchar(19) DEFAULT NULL,
  PRIMARY KEY (`year`,`period`,`stock_cd`,`data_sour`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `curr_listed_corp`
--

DROP TABLE IF EXISTS `curr_listed_corp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `curr_listed_corp` (
  `stock_cd` varchar(6) NOT NULL,
  `data_sour` varchar(20) DEFAULT NULL,
  `stock_sname` varchar(10) DEFAULT NULL,
  `corp_sname` varchar(100) DEFAULT NULL,
  `corp_name` varchar(500) DEFAULT NULL,
  `indus` varchar(100) DEFAULT NULL,
  `market_part` char(5) DEFAULT NULL,
  PRIMARY KEY (`stock_cd`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_source`
--

DROP TABLE IF EXISTS `data_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_source` (
  `code` int(11) DEFAULT NULL,
  `name` varchar(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `listed_corp_info`
--

DROP TABLE IF EXISTS `listed_corp_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `listed_corp_info` (
  `data_sour` varchar(20) NOT NULL,
  `year` char(4) NOT NULL,
  `period` varchar(8) NOT NULL,
  `stock_cd` varchar(6) NOT NULL,
  `stock_sname` varchar(20) DEFAULT NULL,
  `corp_sname` varchar(50) DEFAULT NULL,
  `corp_name` varchar(500) DEFAULT NULL,
  `eh_name` varchar(100) DEFAULT NULL,
  `indus` varchar(50) DEFAULT NULL,
  `reg_addr` varchar(1000) DEFAULT NULL,
  `corp_url` varchar(200) DEFAULT NULL,
  `legal_reps` varchar(500) DEFAULT NULL,
  `corp_sec` varchar(10) DEFAULT NULL,
  `reg_cap` decimal(24,2) DEFAULT NULL,
  `post_cd` varchar(6) DEFAULT NULL,
  `corp_tel` varchar(500) DEFAULT NULL,
  `corp_fax` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `listed_time` char(10) DEFAULT NULL,
  `raise_cap` char(10) DEFAULT NULL,
  `issue_qty` int(11) DEFAULT NULL,
  `issue_price` decimal(24,2) DEFAULT NULL,
  `issue_pe_ratio` decimal(12,6) DEFAULT NULL,
  `issue_way` varchar(200) DEFAULT NULL,
  `main_underw` varchar(200) DEFAULT NULL,
  `listed_referr` varchar(50) DEFAULT NULL,
  `recomm_org` varchar(100) DEFAULT NULL,
  `modifytime` varchar(19) DEFAULT NULL,
  PRIMARY KEY (`data_sour`,`year`,`period`,`stock_cd`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `market_parts`
--

DROP TABLE IF EXISTS `market_parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `market_parts` (
  `code` char(5) DEFAULT NULL,
  `name` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `period_list`
--

DROP TABLE IF EXISTS `period_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `period_list` (
  `year` char(4) DEFAULT NULL,
  `period` varchar(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `profit_table`
--

DROP TABLE IF EXISTS `profit_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profit_table` (
  `year` char(4) NOT NULL,
  `period` varchar(8) NOT NULL,
  `stock_cd` varchar(6) NOT NULL,
  `data_sour` varchar(20) NOT NULL,
  `biz_income` decimal(24,2) DEFAULT NULL,
  `biz_cost` decimal(24,2) DEFAULT NULL,
  `sell_cost` decimal(24,2) DEFAULT NULL,
  `manage_cost` decimal(24,2) DEFAULT NULL,
  `explor_cost` decimal(24,2) DEFAULT NULL,
  `fin_cost` decimal(24,2) DEFAULT NULL,
  `ast_devalu_loss` decimal(24,2) DEFAULT NULL,
  `fair_value_chng_net_inc` decimal(24,2) DEFAULT NULL,
  `inv_prft` decimal(24,2) DEFAULT NULL,
  `invest_assoc_joint_comp` decimal(24,2) DEFAULT NULL,
  `operat_prft_oth_subj` decimal(24,2) DEFAULT NULL,
  `run_prft` decimal(24,2) DEFAULT NULL,
  `subs_reven` decimal(24,2) DEFAULT NULL,
  `nonbiz_incom` decimal(24,2) DEFAULT NULL,
  `nonbiz_cost` decimal(24,2) DEFAULT NULL,
  `ncurrt_ast_dispos_nloss` decimal(24,2) DEFAULT NULL,
  `oth_subj_affect_total_prft` decimal(24,2) DEFAULT NULL,
  `profit_tamt` decimal(24,2) DEFAULT NULL,
  `income_tax` decimal(24,2) DEFAULT NULL,
  `oth_subj_affect_net_prft` decimal(24,2) DEFAULT NULL,
  `net_profit` decimal(24,2) DEFAULT NULL,
  `nprf_attrib_parent_corp` decimal(24,2) DEFAULT NULL,
  `less_intr_income` decimal(24,2) DEFAULT NULL,
  `modifytime` varchar(19) DEFAULT NULL,
  PRIMARY KEY (`year`,`period`,`stock_cd`,`data_sour`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `report_period`
--

DROP TABLE IF EXISTS `report_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `report_period` (
  `code` int(11) DEFAULT NULL,
  `name` varchar(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `spider_process_info`
--

DROP TABLE IF EXISTS `spider_process_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spider_process_info` (
  `corp_stock_cd` varchar(6) DEFAULT NULL,
  `year` char(4) DEFAULT NULL,
  `period` varchar(8) DEFAULT NULL,
  `Data_Sour` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
