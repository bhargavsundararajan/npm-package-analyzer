library(alr3)
library(GGally)

my_data <- read.csv(file="npm_repo_data.csv", header=TRUE, sep=",")

my_data$tlag[my_data$tlag < 0] <- my_data$tlag[my_data$tlag < 0] * -1

plot(density(my_data$lines_of_code),main="Density plot of LOC before log")
my_data$lines_of_code <- log(my_data$lines_of_code)
plot(density(my_data$lines_of_code),main="Density plot of LOC after log")

scatter.smooth(y=my_data$lines_of_code, x=my_data$deps_depth, main="LOC ~ Depth")
plot(density(my_data$cyclomatic_complexity), main="Density plot of CC before log")
my_data$cyclomatic_complexity <- log(my_data$cyclomatic_complexity)
plot(density(my_data$cyclomatic_complexity),main="Density plot of CC after log")

plot(density(my_data$tlag))
my_data$tlag <- log(my_data$tlag)
plot(density(my_data$tlag))
my_data$tlag <- exp(my_data$tlag)
plot(density(my_data$tlag))

plot(density(my_data$deps_depth))

cor(my_data$lines_of_code,my_data$cyclomatic_complexity)
cor(my_data$lines_of_code,my_data$tlag)
cor(my_data$cyclomatic_complexity,my_data$tlag)



outliers <- boxplot(my_data$lines_of_code, plot = FALSE)$out
my_data <- my_data[-which(my_data$lines_of_code %in% outliers),]
outliers <- boxplot(my_data$lines_of_code, plot = FALSE)$out
boxplot(my_data$lines_of_code)

boxplot(my_data$tlag)
outliers <- boxplot(my_data$tlag, plot = FALSE)$out
my_data <- my_data[-which(my_data$tlag %in% outliers),]
boxplot(my_data$tlag)

boxplot(my_data$deps_depth)
outliers <- boxplot(my_data$deps_depth, plot = FALSE)$out
my_data <- my_data[-which(my_data$deps_depth %in% outliers),]
boxplot(my_data$deps_depth)

model = lm(deps_depth ~ lines_of_code + tlag, data = my_data)
summary(model)

cooksd <- cooks.distance(model)
sample_size <- nrow(my_data)
influential <- as.numeric(names(cooksd)[(cooksd > (4/sample_size))])

my_data = my_data[-influential, ]


model = lm(deps_depth ~ lines_of_code + tlag, data = my_data)
summary(model)

res <- resid(model)
plot(density(res),"Density plot of Residuals")


my_data$deps_depth <- log(my_data$deps_depth)
model = lm(deps_depth ~ lines_of_code + tlag, data = my_data)
summary(model)
res <- resid(model)
plot(density(res))
