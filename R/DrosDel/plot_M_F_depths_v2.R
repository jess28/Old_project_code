# Basic plots of pooled male/female DrosDel read depths.
# Copyright (C) 2014 Jessica Strein, jessica.strein@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# This code is not meant to be run as a full program, it is simple a list of all
# commands taken to create plots of male vs female Drosophila read depths.
###############################################################################
# functions
###############################################################################
# A generic barplot function
barp <- function(x, ymax, ylab, xlab, color, names,  mn) {
    barplot(x,
            xlab=xlab,
            ylab=ylab,
            ylim=c(0,ymax),
            col=color,
            border=NA,
            names.arg=names,
            main=mn,
            axisnames=TRUE)
}


############################################################################
# Load data
############################################################################
male_file <- "pair_m_v6_10kb.tab.gz"
female_file <- "pair_f_v6_10kb.tab.gz"
m <- read.table(gzfile(male_file),
                sep="\t",
                header=TRUE,
                na.strings="NA",
                stringsAsFactors=FALSE)
f <- read.table(gzfile(female_file),
                sep="\t",
                header=TRUE,
                na.strings="NA",
                stringsAsFactors=FALSE)
names(m)
names(f)

mnames <- names(m)[-1]
for(i in mnames){
    m[[i]] <- as.numeric(m[[i]])
}
fnames <- names(f)[-1]
for(i in fnames){
    f[[i]] <- as.numeric(f[[i]])
}

fig_base <- "/home/jessstrein/Dropbox/chor_figs/"

cg_file <- "/home/jessstrein/Storage/JessWork/DrosDel/references/10kb_ref_gc_v6.tab.gz"

rmcg_file <- 'RepeatMaskedNcont.tab'
rmcg <- read.table(rmcg_file,
                   sep="\t",
                   header=TRUE,
                   stringsAsFactors=FALSE)

############################################################################
# summaries
############################################################################
summary(m)
summary(f)

############################################################################
# plots
############################################################################
# creates big initial plot of one data set
plot(m$mean_dp, type="l")
comb <- paste(m$chrom, m$window, sep="_")

pdf("drosdelall.pdf", height=8, width=11)

par(mfrow=c(2,1))
barplot(m$mean_dp[1:length(m$mean_dp)], ylim=c(0,550), col="blue", border=NA)
barplot(f$mean_dp[1:length(m$mean_dp)], ylim=c(0,550), col="red", border=NA)

dev.off()


# try to make something more complex
# creates bar plots for each chromosome
chroms <- levels(as.factor(m$chrom))

head(as.factor(m$chrom))
chroms <- chroms[-15]
chroms <- chroms[-14]
chroms <- chroms[-12]
chroms <- chroms[-11]
chroms <- chroms[-10] # remove the high-coverage mt
chroms <- chroms[-8] # remove the 2/3 het chroms for the moment...
chroms <- chroms[-6] # remove the 2/3 het chroms for the moment...
chroms <- chroms[-4] # remove the 2/3 het chroms for the moment...
chroms <- chroms[-2] # remove the 2/3 het chroms for the moment...
print(chroms)

white <- c("2R", "3R", "2L", "3L", "4", "X")

name <- paste(fig_base, "totv6_10kb_byChrom.pdf", sep="")
pdf(name, height=8, width=11)

layout(matrix(seq(1,(2*length(white))),4,3, byrow=FALSE))

par(mar=c(2,4,4,0), oma=c(1,1,1,1))
for(i in 1:length(white)) {
    if(i < 3){
        ylab <- paste("Avg", "depth", sep="_")
    } else{
        ylab <- ""
    }
    n <- NA
    subm <- subset.data.frame(m, m$chrom == white[i])
    subf <- subset.data.frame(f, f$chrom == white[i])
    maxm <- max(subm$mean_dp, na.rm=TRUE)
    maxf <- max(subf$mean_dp, na.rm=TRUE)
    ymax <- max(c(maxm, maxf)) + (0.1 * max(c(maxm, maxf)))
    label <- paste(as.character(white[i]), "M", sep="_")
    xlab <- ""
    barp(subm$mean_dp, ymax, ylab, xlab, "blue", n, label)
    box()
    if(i%%2 == 0){
            xlab <- mtext("Position", side=1, line=15, outer=FALSE, at=NA,
            adj=NA, padj=NA, cex=0.7, font=NA)
    } else{
            xlab <- ""
    }
    label <- paste(as.character(white[i]), "F", sep="_")
    barp(subf$mean_dp, ymax, ylab, xlab, "red", n, label)
    box()
}

dev.off()

name <- paste(fig_base, "X_10kb_end.pdf", sep="")
pdf(name, height=8, width = 11)
layout(matrix(seq(1,2),2,1, byrow=FALSE))
par(mar(6,4,4,2))
secm <- subset.data.frame(m, m$chrom == "X" & m$win >= 1350 & m$win <=1450)
secf <- subset.data.frame(f, f$chrom == "X" & f$win >= 1350 & f$win <=1450)
maxm <- max(secm$mean_dp, na.rm=TRUE)
maxf <- max(secf$mean_dp, na.rm=TRUE)
ymax <- max(c(maxm, maxf)) + (0.1 * max(c(maxm, maxf)))
label <- paste("X", "M", sep="_")
xlab <- ""
n <- rep(NA, length(secf$mean_dp))
for(i in 1:length(secf$mean_dp)){
   if(i%%20 == 0){
       n[i] <- i + 1350
   } else{
       n[i] <- ""
   }
}
mplot <- barp(secm$mean_dp, ymax, ylab, xlab, "blue", n, label)
box()
label <- paste("X", "F", sep="_")
xlab <- "windows"
fplot <- barp(secf$mean_dp, ymax, ylab, xlab, "red", n, label)
axis(1, at=fplot, labels=n, las=2)
box()
dev.off()

white <- c("2R", "3R", "2L", "3L", "4", "X")
keeps <- data.frame()
for(i in 1:length(m$chrom)) {
    tmp <- m[i,]
    if(tmp$chrom %in% white) {
        keeps <- rbind(keeps, tmp)
    }
}
femk <- data.frame()
for(i in 1:length(f$chrom)) {
    tmp <- f[i,]
    if(tmp$chrom %in% white) {
        femk <- rbind(femk, tmp)
    }
}

cg <- data.frame()
for(i in 1:length(rmcg$chrom)) {
    tmp <- rmcg[i,]
    if(tmp$chrom %in% white) {
        cg <- rbind(cg, tmp)
    }
}

xN <- subset.data.frame(cg, cg$chrom == 'X')
aN <- subset.data.frame(cg, cg$chrom != 'X')

chpick <- function(x) if(x[1] %in% white, rbind(x))
keeps <- data.frame(apply(m, 1, chpick))
femk <- data.frame(apply(f, 1, chpick))

chroms <- levels(as.factor(keeps$chrom))
past <- ""
brk <- vector()
cumul <- 0
for(i in 1:length(keeps$chrom)) {
    tmp <- keeps[i,]
    if(tmp$chrom != past) {
        brk <- c(brk, i)
        past <- tmp$chrom
    }
}
print(brk)

rat <- log((keeps$mean_dp/2.02803918)/(femk$mean_dp/2.47324031))
plot(rat, type="l")
abline(v=brk, col="gray")

# standard error
stderrm <- sqrt(keeps$dp_var/keeps$num_bp)
stderrf <- sqrt(femk$dp_var/femk$num_bp)
stderr <- sqrt(stderrm^2 + stderrf^2)
df <- (stderr^4)/((stderrm^4)/(keeps$num_bp -1) + (stderrf^4)/(femk$num_bp -1))
head(stderr)
head(df)

# t-test
ymean <- femk$mean_dp/0.975015993
xmean <- keeps$mean_dp/1.036784679
mfmean <- xmean - ymean
tstat <- mfmean/stderr
head(tstat)

# p value
pval <- 2 * pt(-abs(tstat), df)

# conf int
cint <- qt(1 - 0.25, df)
cintl <- tstat - cint
cintu <- tstat + cint
lcl <- cintl * stderr
ucl <- cintu * stderr
head(lcl)
head(ucl)

# adjust p to q
q <- p.adjust(pval, method="fdr")

# data frame
ptdf <- data.frame(chrom = femk$chrom,
                   win = femk$window,
                   m_num = keeps$num_bp,
                   f_num = femk$num_bp,
                   m_mean = xmean,
                   f_mean = ymean,
                   mf_diff = mfmean,
                   m_sd = keeps$dp_sd,
                   f_sd = femk$dp_sd,
                   lcl = lcl,
                   ucl = ucl,
                   tstat = tstat,
                   pval = pval,
                   qval = q)

auto <- subset.data.frame(ptdf, ptdf$chrom != "X")

adj_f_mean <- auto$f_mean * (mean((auto$m_mean/auto$f_mean), na.rm=T))
adj_mf_diff <- auto$m_mean - adj_f_mean

# standard error
stderrm <- sqrt((auto$m_sd^2)/auto$m_num)
stderrf <- sqrt((auto$f_sd^2)/auto$f_num)
stderr <- sqrt(stderrm^2 + stderrf^2)
df <- (stderr^4)/((stderrm^4)/(auto$m_num -1) + (stderrf^4)/(auto$f_num -1))

# t-test
tstat <- adj_mf_diff/stderr

# p value
pval <- 2 * pt(-abs(tstat), df)

# conf int
cint <- qt(1 - 0.25, df)
cintl <- tstat - cint
cintu <- tstat + cint
lcl <- cintl * stderr
ucl <- cintu * stderr

# adjust p to q
q <- p.adjust(pval, method="fdr")

autosome <- data.frame(chrom = auto$chrom,
                       win = auto$win,
                       m_num = auto$m_num,
                       f_num = auto$f_num,
                       m_mean = auto$m_mean,
                       f_mean = adj_f_mean,
                       mf_diff = adj_mf_diff,
                       m_sd = auto$m_sd,
                       f_sd = auto$f_sd,
                       lcl = lcl,
                       ucl = ucl,
                       tstat = tstat,
                       pval =pval,
                       qval = q)

chromx <- subset.data.frame(ptdf, ptdf$chrom == "X")

adj_fx_mean <- chromx$f_mean * (mean((chromx$m_mean/chromx$f_mean), na.rm=T))
adj_mfx_diff <- chromx$m_mean - adj_fx_mean

# standard error
stderrm <- sqrt((chromx$m_sd^2)/chromx$m_num)
stderrf <- sqrt((chromx$f_sd^2)/chromx$f_num)
stderr <- sqrt(stderrm^2 + stderrf^2)
df <- (stderr^4)/((stderrm^4)/(chromx$m_num -1) + (stderrf^4)/(chromx$f_num -1))

# t-test
tstat <- adj_mfx_diff/stderr

# p value
pval <- 2 * pt(-abs(tstat), df)

# conf int
cint <- qt(1 - 0.25, df)
cintl <- tstat - cint
cintu <- tstat + cint
lcl <- cintl * stderr
ucl <- cintu * stderr

# adjust p to q
q <- p.adjust(pval, method="fdr")

Xchrom <- data.frame(chrom = chromx$chrom,
                     win = chromx$win,
                     m_num = chromx$m_num,
                     f_num = chromx$f_num,
                     m_mean = chromx$m_mean,
                     f_mean = adj_fx_mean,
                     mf_diff = adj_mfx_diff,
                     m_sd = chromx$m_sd,
                     f_sd = chromx$f_sd,
                     lcl = lcl,
                     ucl = ucl,
                     tstat = tstat,
                     pval =pval,
                     qval = q)

for(i in c(0.05, 0.08, 0.1)) {
    for(j in c(1e-5, 1e-6, 1e-7, 1e-8)) {
        sz <- subset.data.frame(autosome, autosome$m_num > 500)
        sub <- subset.data.frame(sz, log(sz$m_mean/sz$f_mean) > i)
        subtot <- subset.data.frame(sub, sub$qval < j)
        bb <- c(i, j, dim(subtot))
        print(bb)
    }
}

for(i in c(0.1, 0.11, 0.15)) {
    for(j in c(1e-5, 1e-6, 1e-7, 1e-8)) {
        sz <- subset.data.frame(Xchrom, Xchrom$m_num > 500)
        sub <- subset.data.frame(sz, log(sz$m_mean/sz$f_mean) > i)
        subtot <- subset.data.frame(sub, sub$qval < j)
        bb <- c(i, j, dim(subtot))
        print(bb)
    }
}

sz1 <- subset.data.frame(Xchrom, Xchrom$m_num > 5000)
sub1 <- subset.data.frame(sz1, log2(sz1$m_mean/sz1$f_mean) < -0.58)
subtot1 <- subset.data.frame(sub1, sub1$qval < 1e-7)
print(subtot1)

sz2 <- subset.data.frame(Xchrom, Xchrom$m_num > 5000)
sub2 <- subset.data.frame(sz2, log2(sz2$m_mean/sz2$f_mean) > 0.58)
subtot2 <- subset.data.frame(sub2, sub2$qval < 1e-7)
print(subtot2)

sz3 <- subset.data.frame(autosome, autosome$m_num > 5000)
sub3 <- subset.data.frame(sz3, log2(sz3$m_mean/sz3$f_mean) < log2(1/1.2))
subtot3 <- subset.data.frame(sub3, sub3$qval < 1e-7)
print(subtot3)

sz4 <- subset.data.frame(autosome, autosome$m_num > 5000)
sub4 <- subset.data.frame(sz4, log2(sz4$m_mean/sz4$f_mean) > 0.58)
subtot4 <- subset.data.frame(sub4, sub4$qval < 1e-7)
print(subtot4)

allbio <- data.frame()
for(i in 1:length(subtot1$chrom)) {
    tmp <- subtot1[i,]
    allbio <- rbind(allbio, tmp)
}
for(i in 1:length(subtot2$chrom)) {
    tmp <- subtot2[i,]
    allbio <- rbind(allbio, tmp)
}
for(i in 1:length(subtot3$chrom)) {
    tmp <- subtot3[i,]
    allbio <- rbind(allbio, tmp)
}

# deal with sqlite data
library("RSQLite")
drv <- dbDriver("SQLite")
con <- dbConnect(drv,
       "/home/jessstrein/Storage/Data/DrosDel_data/refgenome/drosdel_db/drosdel.db")
refgc <- dbGetQuery(con, "Select CG as CG, Chrom as chrom, Window as win from
                    refseq1kb")

refgc <- read.table(gzfile(cg_file),
                sep="\t",
                header=TRUE,
                na.strings="NA",
                stringsAsFactors=FALSE)
xcg <- subset.data.frame(refgc, refgc$chrom == "X")
apart <- subset.data.frame(refgc, refgc$chrom != "X")
acg <- data.frame()
for(i in 1:length(apart$chrom)) {
    tmp <- apart[i,]
    if(tmp$chrom %in% white) {
        acg <- rbind(acg, tmp)
    }
}

cgname <- paste(fig_base, "RepeatMaskerN.pdf", sep="")
pdf(cgname, height=8, width=11)
par(mar=c(0, 4, 4, 2), fin=c(10, 2.5))
plot(xN$win, xN$n_per, type='n', xlab='', ylab='N content of masker', xaxt='n',
     ylim=c(0, 1))
lines(xN$win, xN$n_per, type='l', lwd=1.5, col='orange')
plot(aN$n_per, type='n', xlab='', ylab='N content of masker', xaxt='n',
     ylim=c(0, 1))
lines(aN$n_per, type='l', lwd=1.5, col='orange')
abline(v=as.numeric(chromosomes), col="black")
dev.off()

Nname <- paste(fig_base, "Nagainstrat.png", sep="")
png(Nname, height=1000, width=1000)
ratio <- log2(Xchrom$m_mean/Xchrom$f_mean)
plot(ratio, xN$n_per, xlab='log2 ratio of male to female depth on X',
     ylab='repeat content', col=(ifelse(ratio %in% s1rat & Xchrom$f_num > 500, 'red',
     ifelse(ratio %in% s2rat & Xchrom$m_num > 500, 'blue', 'black'))), pch=19)
dev.off()

Nname <- paste(fig_base, "aNagainstrat.png", sep="")
png(Nname, height=1000, width=1000)
ratio <- log2(autosome$m_mean/autosome$f_mean)
plot(ratio, aN$n_per, xlab='log2 ratio of male to female depth on autosomes',
     ylab='repeat content', col=(ifelse(ratio %in% s3rat & autosome$f_num > 500, 'red',
     ifelse(ratio %in% s4rat & autosome$m_num > 500, 'blue', 'black'))), pch=19)
dev.off()

Nname <- paste(fig_base, "NvsMale.jpeg", sep="")
jpeg(Nname, height=1000, width=1000)
ratio <- log2(Xchrom$m_mean/Xchrom$f_mean)
plot(Xchrom$m_mean, xN$n_per, xlab='male depth on the X', ylab='repeat content')
dev.off()

qq <- data.frame(ratio, xN$n_per)
is.numeric(xN$n_per)
qa <-
cor(qq, use="complete")

xname <- paste(fig_base, "xchr_pairv6_10kb.pdf", sep="")
pdf(xname, height=8, width=11)

par(mar=c(0, 4, 4, 2), fin=c(10, 2.5))
plot(xcg$win, xcg$gc_per, type='n', xlab="", ylab="CG content of ref", xaxt='n',
     ylim=c(0,1))
lines(xcg$win, xcg$gc_per, type='l', lwd=1.5, col="green")

par(mar=c(0, 4, 0, 2), fin=c(10, 5))
ratio <- log2(Xchrom$m_mean/Xchrom$f_mean)

s1rat <- log2(subtot1$m_mean/subtot1$f_mean)
s2rat <- log2(subtot2$m_mean/subtot2$f_mean)

plot(ratio, col=(ifelse(ratio %in% s1rat & Xchrom$f_num > 5000, 'red',
     ifelse(ratio %in% s2rat & Xchrom$m_num > 5000, 'blue', 'black'))),
     pch=(ifelse(Xchrom$m_num < 5000, 21, ifelse(Xchrom$qval > 1e-7, 8, 19))), xlab='',
     ylab="log2 ratio of male to female depth", xaxt='n')

par(mar=c(4, 4, 0, 2), fin=c(10,2.5))
plot(Xchrom$win, log(Xchrom$m_num/Xchrom$f_num), type='n', xlab="window number on X",
     ylab="number of covered bases")
lines(Xchrom$win, log(Xchrom$m_num/Xchrom$f_num), type="l", lwd=1.5, col="darkorchid4")

dev.off()

aname <- paste(fig_base, "auto_pairv6_10kb.pdf", sep="")
pdf(aname, height=8, width=11)

c <- ""
chromosomes <- ""
for(i in 1:length(autosome$chrom)) {
    if(autosome$chrom[i] != c) {
        chromosomes <- c(chromosomes, i)
        c <- autosome$chrom[i]
    }
}

par(mar=c(0, 4, 4, 2), fin=c(10, 2.5))
plot(acg$gc_per, type='n', xlab="", ylab="CG content of ref", xaxt='n',
     ylim=c(0.,1))
lines(acg$gc_per, type='l', lwd=1.5, col="green")
abline(v=as.numeric(chromosomes), col="grey")

par(mar=c(0, 4, 0, 2), fin=c(10, 5))
ratio <- log(autosome$m_mean/autosome$f_mean)

s3rat <- log(subtot3$m_mean/subtot3$f_mean)
s4rat <- log(subtot4$m_mean/subtot4$f_mean)

plot(ratio, col=(ifelse(ratio %in% s3rat & autosome$f_num > 5000, 'red',
     ifelse(ratio %in% s4rat & autosome$m_num > 5000, 'blue', 'black'))),
     pch=(ifelse(autosome$m_num < 5000, 21, ifelse(autosome$qval > 1e-7, 8, 19))),
     xlab="", ylab="log2 ratio of male to female depth", xaxt="n")
abline(v=as.numeric(chromosomes), col="grey")

par(mar=c(4, 4, 0, 2), fin=c(10,2.5))
plot(log(autosome$m_num/autosome$f_num), type='n', xlab="window number",
     ylab="number of covered bases")
lines(log(autosome$m_num/autosome$f_num), type='l', lwd=1.5,
      col="darkorchid4")
abline(v=as.numeric(chromosomes), col="grey")

dev.off()
