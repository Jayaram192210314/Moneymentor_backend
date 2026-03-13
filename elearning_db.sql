-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 13, 2026 at 04:25 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `elearning_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `goals`
--

CREATE TABLE `goals` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `goal_name` varchar(255) NOT NULL,
  `target_amount` decimal(12,2) NOT NULL,
  `already_saved_amount` decimal(12,2) NOT NULL,
  `deadline` date NOT NULL,
  `extra_amount` decimal(12,2) DEFAULT 0.00,
  `withdraw_amount` decimal(12,2) DEFAULT 0.00,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `goals`
--

INSERT INTO `goals` (`id`, `user_id`, `goal_name`, `target_amount`, `already_saved_amount`, `deadline`, `extra_amount`, `withdraw_amount`, `created_at`) VALUES
(1, 4, 'Buy Bike', 50000.00, 10000.00, '2026-03-28', 0.00, 0.00, '2026-02-27 10:24:48'),
(2, 3, 'Car', 500000.00, 105000.00, '2027-02-27', 10000.00, 5000.00, '2026-02-27 10:30:42'),
(3, 3, 'New Car', 100000.00, 10000.00, '2026-03-31', 0.00, 0.00, '2026-03-05 14:38:35'),
(7, 7, 'Thar Repair', 50000.00, 10000.00, '2026-03-31', 0.00, 0.00, '2026-03-12 04:39:40');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `time_value` varchar(20) NOT NULL,
  `type` varchar(50) NOT NULL,
  `is_unread` tinyint(1) DEFAULT 1,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `title`, `message`, `time_value`, `type`, `is_unread`, `created_at`) VALUES
(95, 3, 'Daily Tip', 'Check out your daily financial tip!', '8:15 AM', 'daily', 1, '2026-03-13 08:15:15'),
(96, 3, 'Monthly Goal', 'It\'s time to update your savings goal!', '8:20 AM', 'monthly', 1, '2026-03-13 08:20:15'),
(97, 4, 'Daily Tip', 'Check out your daily financial tip!', '8:35 AM', 'daily', 1, '2026-03-13 08:35:15'),
(98, 4, 'Monthly Goal', 'It\'s time to update your savings goal!', '8:40 AM', 'monthly', 1, '2026-03-13 08:40:15');

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(190) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `dob` date DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `email` varchar(190) NOT NULL,
  `password` varchar(170) NOT NULL,
  `otp` varchar(50) DEFAULT NULL,
  `otp_expiry` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `full_name`, `dob`, `mobile`, `email`, `password`, `otp`, `otp_expiry`) VALUES
(1, 'Jaya Ram', '2005-06-04', '98765432190', 'jaya@example.com', 'scrypt:32768:8:1$1iH8WFJ8fxt1IZ1R$d79007c733c51f5a843845e06d1049c429ec4a225d6bb3fa6ab8092cd856764619f24d618f04109f08fd7cdb9fe480e9e5ebe349c0d60ab546d9e85b514e0339', '8599', '2026-02-19 13:37:01.230411'),
(2, 'Kumar R', '2002-05-10', '9876543210', 'kumar@example.com', 'scrypt:32768:8:1$QQCb6lP0yoKa9GXv$2b140478c3b2a1e18bea3fc4f73f2702751f5a27e58b67b5b91c5dd201acf4b3823217246f54ccd17fda852eab03d0d418dca8bbe9603dc59c4f946eecdbeb16', NULL, NULL),
(3, 'Jay', '2005-06-04', '9876543210', 'jayaramklv@gmail.com', 'scrypt:32768:8:1$STox9z4PWJd6hZqv$785009aa9f3f5ec4811398d2ce7c4ce3c21dc252250d1c176d282e202ddd77598cbc364d0dee5a40e317638427b27365572207dfda968b2ca240cff828240a6a', '8473', '2026-03-11 09:36:54.617732'),
(4, 'Viraj Shambhu', '2005-06-04', '9876543210', 'sn3029769@gmail.com', 'scrypt:32768:8:1$MAQ3sluKxlUA7tkd$5e0905c4001ac71c8da6e494a4102cb17dfd69f9a452f097e36a923cd77d023659af28f54b27890e2a26dd65d9e243ce0de02f9de1a8d50e5e88d17258d033b3', NULL, NULL),
(5, 'Kudipudi Sandeep', '2005-02-15', '9812341230', 'Sandeep0206@gmail.com', 'scrypt:32768:8:1$q3QIBuxMcTPp0ATt$8e35c3f8459d0c65a46ebb38f677f915fb336af15b0d9c083ae5f65d8fd2e935df49e1f25a30846b6831b5c02bba48c25464467a26e74b24819a9de779ce2ab0', NULL, NULL),
(7, 'Dev', '2024-01-19', '9866333666', 'spacelife8989@gmail.com', 'scrypt:32768:8:1$miomEph2dHz62AW0$a71ce0a1a72bde22eee4f956d2183a48c87137c9c85aeb147c92d5832d28520bbd1a85102311e98d803510e59dc9f066b39d3e3dcf43055e55714b5d6e8a824c', NULL, NULL),
(8, 'Test User', '1990-01-01', '1234567890', 'test@example.com', 'scrypt:32768:8:1$Q9e3nD3Hdm6klfQL$4daa0dbe03e926445b73f590c9577af48b618a81e525c4e9c11f8642488dcd12a2535de1a48cacbbfa0b696aeb7c7c0140151f59588dfadcfb8b26426d49ae7e', NULL, NULL),
(9, 'Test Fix', '1995-05-05', '1234567890', 'testfix@example.com', 'scrypt:32768:8:1$2sDtTpprKIFrLufA$b250f07369d5896617d0b4d60bc401d529d1a7ad7a02ea5decf3d397831c1e926f3e570c76533d5a69a37adc32afb3df66c0d54394cb24539579657bd6086029', NULL, NULL),
(10, 'Tester User', '1995-10-10', '9876543210', 'testuser@example.com', 'scrypt:32768:8:1$1ZFslU07ephc1CEw$816338bd0ba5f80b17bb574811d898a17b48771e8c55d992c525732c31b06d23b52c9ab8fd6d00cbb39654e291af9b68a502c03a4aaebcf177ff3b12ccdb26a6', NULL, NULL),
(11, 'John Doe', '1990-01-01', '1234567890', 'john@example.com', 'scrypt:32768:8:1$bWpIEzM6TWPp6QnW$9ba3925746980254f3acd8ef46450d7850099f05fc4d683592537e68bd2573d8d212f4b98e6eabf40ef77d545723c8642d4c1a066b98feede6656404e31e88ff', NULL, NULL),
(12, 'chotu', '2005-03-19', '9640638489', 'kousikssvv34@gmail.com', 'scrypt:32768:8:1$pn1WesPaVyNAo989$2c1f4103d91a4d033d45f6fa4e689a6ba7d53a71fa2f2fb55ce815b9f795498f7a1b0099d7726dc7903b2c87d3e640e227330ece0a8cb4e4ba53fd7c2831fd5d', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `terms`
--

CREATE TABLE `terms` (
  `id` int(11) NOT NULL,
  `term_text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `terms`
--

INSERT INTO `terms` (`id`, `term_text`) VALUES
(1, 'Asset - Anything you own that has value.'),
(2, 'Liability - Money you owe to others.'),
(3, 'Equity - Ownership value in a business or asset.'),
(4, 'Income - Money you earn.'),
(5, 'Expense - Money you spend.'),
(6, 'Budget - A plan for income and expenses.'),
(7, 'Savings - Money kept aside for future use.'),
(8, 'Investment - Putting money into something to help it grow.'),
(9, 'Interest - Extra money paid for borrowing or earned from saving.'),
(10, 'Inflation - Increase in prices over time.'),
(11, 'Net Worth - Total assets minus total liabilities.'),
(12, 'Credit Score - A number showing how reliable you are in repaying loans.'),
(13, 'Loan - Borrowed money that must be repaid.'),
(14, 'EMI - Fixed monthly loan repayment amount.'),
(15, 'Collateral - Asset pledged as security for a loan.'),
(16, 'Insurance - Protection against financial loss.'),
(17, 'Premium - Amount paid regularly for insurance.'),
(18, 'Deductible - Amount you pay before insurance coverage starts.'),
(19, 'Revenue - Total income earned by a business.'),
(20, 'Profit - Amount left after expenses are deducted from revenue.'),
(21, 'Loss - When expenses exceed income.'),
(22, 'Cash Flow - Movement of money in and out.'),
(23, 'Dividend - Profit shared with shareholders.'),
(24, 'Stock - A share representing ownership in a company.'),
(25, 'Bond - A loan to a company/government with fixed interest.'),
(26, 'Mutual Fund - A pool of money invested in stocks, bonds, etc.'),
(27, 'SIP - Systematic monthly investment into mutual funds.'),
(28, 'ETF - A fund traded like a stock on the exchange.'),
(29, 'Portfolio - Collection of investments.'),
(30, 'Risk - Chance of losing money.'),
(31, 'Return - Profit earned from an investment.'),
(32, 'Capital - Money used to start or run a business.'),
(33, 'Depreciation - Decrease in asset value over time.'),
(34, 'Appreciation - Increase in asset value over time.'),
(35, 'Diversification - Spreading investments to reduce risk.'),
(36, 'Market Value - Current price of an asset.'),
(37, 'Liquidity - How easily an asset converts to cash.'),
(38, 'Net Income - Income after expenses and taxes.'),
(39, 'Gross Income - Income before any deductions.'),
(40, 'Tax - Money paid to the government.'),
(41, 'Tax Deduction - Reduction in taxable income.'),
(42, 'Tax Exemption - Income not taxed.'),
(43, 'Credit Limit - Maximum amount you can borrow.'),
(44, 'Principal - Original amount invested or borrowed.'),
(45, 'Compound Interest - Interest earned on interest.'),
(46, 'Simple Interest - Interest earned only on principal.'),
(47, 'Overdraft - Withdrawing more than available balance.'),
(48, 'Bankruptcy - Legal state of being unable to pay debts.'),
(49, 'Financial Literacy - Understanding financial concepts.'),
(50, 'Cash Reserve - Emergency money kept aside.'),
(51, 'Fixed Deposit - Deposit locked for a fixed time at interest.'),
(52, 'Recurring Deposit - Monthly saving deposit in a bank.'),
(53, 'Credit Card - Card allowing borrowing up to a limit.'),
(54, 'Debit Card - Card using your bank balance for payments.'),
(55, 'UPI - Instant mobile payment system.'),
(56, 'NEFT - Bank-to-bank fund transfer system.'),
(57, 'RTGS - High-value real-time transfer system.'),
(58, 'IMPS - Instant fund transfer anytime.'),
(59, 'KYC - Verification of customer identity.'),
(60, 'Nominee - Person who receives assets after death.'),
(61, 'Fund Manager - Person managing mutual fund investments.'),
(62, 'Broker - Middleman for buying or selling shares.'),
(63, 'Demat Account - Account holding shares electronically.'),
(64, 'Trading Account - Account used to buy/sell shares.'),
(65, 'Asset Allocation - Distribution of investments.'),
(66, 'Bear Market - Market where prices fall.'),
(67, 'Bull Market - Market where prices rise.'),
(68, 'Expense Ratio - Fee charged by mutual funds.'),
(69, 'Overnight Fund - Fund investing in one-day securities.'),
(70, 'Credit Risk - Risk that borrower may not repay.'),
(71, 'Market Risk - Risk due to market price changes.'),
(72, 'Inflation Risk - Risk of returns losing value due to inflation.'),
(73, 'IPO - First sale of a company\'s shares to the public.'),
(74, 'NAV - Price per unit of a mutual fund.'),
(75, 'Annuity - Regular payment for retirement.'),
(76, 'Pension - Money paid after retirement.'),
(77, 'Working Capital - Money for day-to-day business activities.'),
(78, 'Break-even Point - Point where income equals expenses.'),
(79, 'Asset Class - Category of investment.'),
(80, 'Fiscal Year - Accounting year for taxation.'),
(81, 'Audit - Examination of financial records.'),
(82, 'Subsidy - Financial aid from the government.'),
(83, 'Grant - Money given without repayment.'),
(84, 'Royalty - Payment for using someone\'s work.'),
(85, 'Copyright - Legal protection over creative work.'),
(86, 'Net Banking - Online banking service.'),
(87, 'Inflation Rate - Percentage change in prices.'),
(88, 'CAGR - Yearly growth rate of an investment.'),
(89, 'Balance Sheet - Statement of assets and liabilities.'),
(90, 'Income Statement - Summary of income and expenses.'),
(91, 'Transaction - Any financial activity.'),
(92, 'Statement - Monthly summary of account activity.'),
(93, 'Cheque - A written order for payment.'),
(94, 'Bank Transfer - Moving money between accounts.'),
(95, 'Fraud - Illegal financial deception.'),
(96, 'Scam - Trick to steal money.'),
(97, 'Overvaluation - Asset priced above true value.'),
(98, 'Undervaluation - Asset priced below true value.'),
(99, 'Hedge - Action taken to reduce investment risk.'),
(100, 'Financial Goal - Target set for money planning.');

-- --------------------------------------------------------

--
-- Table structure for table `term_history`
--

CREATE TABLE `term_history` (
  `id` int(11) NOT NULL,
  `term_id` int(11) NOT NULL,
  `shown_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `term_history`
--

INSERT INTO `term_history` (`id`, `term_id`, `shown_date`) VALUES
(2, 73, '2026-02-23'),
(3, 78, '2026-03-01'),
(4, 68, '2026-03-03'),
(5, 10, '2026-03-05'),
(6, 33, '2026-03-10'),
(7, 17, '2026-03-11'),
(8, 76, '2026-03-12');

-- --------------------------------------------------------

--
-- Table structure for table `tips`
--

CREATE TABLE `tips` (
  `id` int(11) NOT NULL,
  `tip_text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tips`
--

INSERT INTO `tips` (`id`, `tip_text`) VALUES
(1, 'Track every rupee you spend to understand your expenses clearly.'),
(2, 'Create a monthly budget and stick to it.'),
(3, 'Build an emergency fund worth 3 to 6 months of expenses.'),
(4, 'Save at least 20% of your income every month.'),
(5, 'Invest early to maximize compound interest.'),
(6, 'Avoid impulse purchases by waiting 24 hours before buying.'),
(7, 'Pay your credit card bills on time to avoid interest.'),
(8, 'Pay off high-interest debt first.'),
(9, 'Set clear short-term and long-term financial goals.'),
(10, 'Review your budget at the end of every month.'),
(11, 'Use UPI and digital payments to track spending easily.'),
(12, 'Limit your EMI commitments to avoid financial strain.'),
(13, 'Invest in mutual funds through SIPs consistently.'),
(14, 'Diversify your investments across asset classes.'),
(15, 'Avoid taking loans for depreciating assets.'),
(16, 'Keep track of your credit score regularly.'),
(17, 'Use cashback and discounts wisely, not impulsively.'),
(18, 'Automate your savings every month.'),
(19, 'Maintain separate accounts for savings and spending.'),
(20, 'Avoid lifestyle inflation as your income grows.'),
(21, 'Cancel unused subscriptions and services.'),
(22, 'Always negotiate prices when possible.'),
(23, 'Avoid co-signing loans for others.'),
(24, 'Compare prices before major purchases.'),
(25, 'Invest in health insurance early.'),
(26, 'Start retirement planning in your 20s.'),
(27, 'Review your investment portfolio yearly.'),
(28, 'Keep learning about personal finance.'),
(29, 'Don\'t chase quick-rich schemes.'),
(30, 'Understand the risks before investing.'),
(31, 'Save bonuses instead of spending them.'),
(32, 'Plan major expenses in advance.'),
(33, 'Avoid emotional decisions in investments.'),
(34, 'Use credit cards only if you can pay in full.'),
(35, 'Start small, but stay consistent with saving.'),
(36, 'Use a financial tracking app.'),
(37, 'Don\'t borrow money to impress others.'),
(38, 'Build multiple income streams.'),
(39, 'Invest in upskilling to increase your earning power.'),
(40, 'Avoid unnecessary bank charges.'),
(41, 'Keep receipts and track tax-related documents.'),
(42, 'Learn basic tax rules in your country.'),
(43, 'Buy term insurance not endowment plans.'),
(44, 'Avoid withdrawing PF unnecessarily.'),
(45, 'Avoid timing the stock market.'),
(46, 'Invest for long term for better returns.'),
(47, 'Don\'t keep too much money idle in savings accounts.'),
(48, 'Use recurring deposits for disciplined saving.'),
(49, 'Invest in gold systematically, not emotionally.'),
(50, 'Spend less than you earn always.'),
(51, 'Follow the 50-30-20 budgeting rule.'),
(52, 'Don\'t compare your finances with others.'),
(53, 'Avoid taking personal loans unless urgent.'),
(54, 'Prioritize needs over wants.'),
(55, 'Track your net worth yearly.'),
(56, 'Learn to say NO to unnecessary outings.'),
(57, 'Keep a financial journal.'),
(58, 'Separate business and personal finances.'),
(59, 'Educate your family about savings.'),
(60, 'Protect your passwords and accounts.'),
(61, 'Avoid get-rich-quick trading signals.'),
(62, 'Don\'t skip EMI payments.'),
(63, 'Buy products only when you need them.'),
(64, 'Invest in index funds as a low-cost option.'),
(65, 'Stop spending on status symbols.'),
(66, 'Review your insurance coverage annually.'),
(67, 'Plan for major life events early.'),
(68, 'Avoid buying gadgets frequently.'),
(69, 'Pay utility bills before the due date.'),
(70, 'Don\'t depend only on one income source.'),
(71, 'Keep liquidity for emergencies.'),
(72, 'Set auto-pay for essential bills.'),
(73, 'Spend cash for small expenses to feel the impact.'),
(74, 'Learn negotiation skills.'),
(75, 'Review bank statements monthly.'),
(76, 'Don\'t lend large amounts to friends or relatives.'),
(77, 'Invest windfalls wisely.'),
(78, 'Spend on experiences, not just things.'),
(79, 'Buy quality products that last.'),
(80, 'Keep a strict limit for entertainment expenses.'),
(81, 'Choose resale-value products when possible.'),
(82, 'Research before investing in real estate.'),
(83, 'Avoid emotional shopping during stress.'),
(84, 'Set up financial goals for each year.'),
(85, 'Don\'t invest in something you don\'t understand.'),
(86, 'Use a shopping list to prevent extra buying.'),
(87, 'Keep documents safely organized.'),
(88, 'Avoid buying extended warranties unnecessarily.'),
(89, 'Don\'t rely solely on advisors learn yourself.'),
(90, 'Save for taxes if your self-employed.'),
(91, 'Limit eating out to save money.'),
(92, 'Start saving for childrens education early.'),
(93, 'Maintain a minimalistic lifestyle.'),
(94, 'Avoid paying interest earn it.'),
(95, 'Plan vacations within your budget.'),
(96, 'Review bank loan offers before deciding.'),
(97, 'Avoid spending for validation from others.'),
(98, 'Use public transport to save money.'),
(99, 'Practice contentment, not comparison.'),
(100, 'Make financial discipline a habit.');

-- --------------------------------------------------------

--
-- Table structure for table `tip_history`
--

CREATE TABLE `tip_history` (
  `id` int(11) NOT NULL,
  `tip_id` int(11) NOT NULL,
  `shown_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tip_history`
--

INSERT INTO `tip_history` (`id`, `tip_id`, `shown_date`) VALUES
(2, 81, '2026-02-23'),
(3, 15, '2026-02-27'),
(4, 29, '2026-03-01'),
(5, 94, '2026-03-02'),
(6, 54, '2026-03-03'),
(7, 99, '2026-03-04'),
(8, 47, '2026-03-05'),
(9, 70, '2026-03-10'),
(10, 17, '2026-03-11'),
(11, 9, '2026-03-12'),
(12, 2, '2026-03-13');

-- --------------------------------------------------------

--
-- Table structure for table `user_article_progress`
--

CREATE TABLE `user_article_progress` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `article_no` int(11) NOT NULL,
  `is_completed` tinyint(1) DEFAULT 0,
  `completed_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_article_progress`
--

INSERT INTO `user_article_progress` (`id`, `user_id`, `article_no`, `is_completed`, `completed_at`) VALUES
(1, 2, 5, 1, '2026-03-01 21:15:08'),
(2, 2, 7, 1, '2026-03-01 21:16:17'),
(3, 3, 2, 1, '2026-03-01 22:14:08'),
(5, 3, 3, 1, '2026-03-01 22:14:17'),
(6, 3, 7, 1, '2026-03-01 22:18:05'),
(7, 3, 8, 1, '2026-03-01 22:18:15'),
(8, 3, 9, 1, '2026-03-01 22:18:24'),
(9, 3, 1, 1, '2026-03-01 22:25:13'),
(10, 3, 4, 1, '2026-03-01 22:25:21'),
(11, 3, 5, 1, '2026-03-01 22:25:24'),
(12, 3, 6, 1, '2026-03-01 22:25:32'),
(13, 3, 10, 1, '2026-03-01 22:25:56'),
(14, 4, 1, 1, '2026-03-01 22:32:46'),
(15, 3, 11, 1, '2026-03-01 23:14:26'),
(16, 3, 12, 1, '2026-03-01 23:14:48'),
(17, 3, 13, 1, '2026-03-05 14:42:21'),
(18, 3, 15, 1, '2026-03-05 14:42:24'),
(19, 3, 16, 1, '2026-03-05 14:42:26'),
(20, 3, 17, 1, '2026-03-05 14:42:27'),
(21, 3, 14, 1, '2026-03-05 14:43:03'),
(22, 3, 84, 1, '2026-03-05 14:44:00'),
(23, 7, 1, 1, '2026-03-11 09:20:46'),
(24, 7, 2, 1, '2026-03-11 09:20:50'),
(29, 7, 3, 1, '2026-03-11 09:30:21'),
(30, 7, 4, 1, '2026-03-11 14:31:15'),
(31, 7, 5, 1, '2026-03-12 00:10:17'),
(32, 7, 6, 1, '2026-03-12 00:10:35'),
(33, 7, 7, 1, '2026-03-12 00:11:06'),
(34, 7, 8, 1, '2026-03-12 00:11:19'),
(35, 7, 9, 1, '2026-03-12 00:27:31'),
(36, 7, 10, 1, '2026-03-12 08:17:38'),
(37, 7, 11, 1, '2026-03-12 08:47:48'),
(38, 7, 12, 1, '2026-03-12 08:48:59'),
(39, 7, 13, 1, '2026-03-12 08:49:25'),
(40, 7, 14, 1, '2026-03-12 08:58:18'),
(41, 7, 15, 1, '2026-03-12 08:59:02'),
(42, 7, 16, 1, '2026-03-12 09:00:33'),
(43, 7, 17, 1, '2026-03-12 09:01:37'),
(44, 7, 18, 1, '2026-03-12 09:03:48'),
(45, 7, 19, 1, '2026-03-12 09:11:37'),
(46, 7, 20, 1, '2026-03-12 09:20:10'),
(47, 7, 21, 1, '2026-03-12 10:11:26'),
(48, 7, 22, 1, '2026-03-12 10:13:17'),
(49, 7, 23, 1, '2026-03-12 10:56:38'),
(50, 7, 24, 1, '2026-03-12 12:32:42'),
(51, 7, 25, 1, '2026-03-12 13:25:43'),
(52, 7, 26, 1, '2026-03-12 14:13:16'),
(53, 7, 27, 1, '2026-03-12 14:39:30'),
(54, 7, 28, 1, '2026-03-12 20:59:51');

-- --------------------------------------------------------

--
-- Table structure for table `user_notifications`
--

CREATE TABLE `user_notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `type` enum('daily','monthly') NOT NULL,
  `time_value` varchar(10) NOT NULL,
  `day_value` int(11) DEFAULT NULL,
  `status` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_notifications`
--

INSERT INTO `user_notifications` (`id`, `user_id`, `type`, `time_value`, `day_value`, `status`) VALUES
(1, 3, 'daily', '8:15 AM', NULL, 0),
(2, 3, 'monthly', '8:20 AM', 13, 0),
(37, 4, 'daily', '8:35 AM', NULL, 1),
(38, 4, 'monthly', '8:40 AM', 13, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `goals`
--
ALTER TABLE `goals`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `register`
--
ALTER TABLE `register`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `terms`
--
ALTER TABLE `terms`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `term_history`
--
ALTER TABLE `term_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `term_id` (`term_id`);

--
-- Indexes for table `tips`
--
ALTER TABLE `tips`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tip_history`
--
ALTER TABLE `tip_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tip_id` (`tip_id`);

--
-- Indexes for table `user_article_progress`
--
ALTER TABLE `user_article_progress`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_user_article` (`user_id`,`article_no`);

--
-- Indexes for table `user_notifications`
--
ALTER TABLE `user_notifications`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`,`type`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `goals`
--
ALTER TABLE `goals`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=99;

--
-- AUTO_INCREMENT for table `register`
--
ALTER TABLE `register`
  MODIFY `id` int(190) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `terms`
--
ALTER TABLE `terms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT for table `term_history`
--
ALTER TABLE `term_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `tips`
--
ALTER TABLE `tips`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT for table `tip_history`
--
ALTER TABLE `tip_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `user_article_progress`
--
ALTER TABLE `user_article_progress`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT for table `user_notifications`
--
ALTER TABLE `user_notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=134;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `goals`
--
ALTER TABLE `goals`
  ADD CONSTRAINT `goals_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `register` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `term_history`
--
ALTER TABLE `term_history`
  ADD CONSTRAINT `term_history_ibfk_1` FOREIGN KEY (`term_id`) REFERENCES `terms` (`id`);

--
-- Constraints for table `tip_history`
--
ALTER TABLE `tip_history`
  ADD CONSTRAINT `tip_history_ibfk_1` FOREIGN KEY (`tip_id`) REFERENCES `tips` (`id`);

--
-- Constraints for table `user_article_progress`
--
ALTER TABLE `user_article_progress`
  ADD CONSTRAINT `user_article_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `register` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
